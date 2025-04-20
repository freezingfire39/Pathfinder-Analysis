import json
import os

import pandas as pd
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from scipy.stats import percentileofscore

from portfolio.factory import OptimizerFactory
from portfolio.portfolio_ import Portfolio
from portfolio.utils import enums
from .serializers import OptimizationInputSerializer, OptimizedPortfolioSerializer, AnalyzerOutputSerializer, \
    CustomInputSerializer, TimingAnalyzerOutputSerializer
import numpy as np
from scipy.optimize import minimize
from django.conf import settings
from portfolio.analyzer import Analyzer
from pathlib import Path
home = str(Path.home())

class OptimizePortfolioView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fdir = settings.RETURNS_DATA_FILE_PATH
        self.rpath = settings.RANK_FILE_PATH
        self.cpath = settings.COMMENTS_FILE_PATH
        self.fac = OptimizerFactory()
        self.score_pair = {
            "vol": self._reverse_score,
            "drawdown_amount": self._reverse_score,
            "beta": self._reverse_score,
            "alpha": self._score,
            "rolling_SR": self._score,
            "annual_return": self._score,
        }
        self.input_serializer_method = OptimizationInputSerializer

    def _score(self, df, col, file):
        p_value = df[col].iloc[-1]
        fpath = os.path.join(self.rpath, file)
        df = pd.read_csv(fpath)
        score = percentileofscore(df["value"].dropna().to_list(), p_value)
        return score

    def _reverse_score(self, df, col, file):
        p_value = df[col].iloc[-1]
        fpath = os.path.join(self.rpath, file)
        df = pd.read_csv(fpath)
        score = 100 - percentileofscore(df["value"].dropna().to_list(), p_value)
        return score

    def generate_porfolio(self, input_serializer):
        symbols = input_serializer.validated_data['symbols']
        capital = input_serializer.validated_data['amount']
        method = input_serializer.validated_data['method']
        if self.fdir is None:
            self.fdir = "D:/workspace/aggregation/"
        if self.rpath is None:
            self.rpath = "D:/workspace/output_search/"
        if self.cpath is None:
            self.cpath = "D:/workspace/comments/"
        p = Portfolio(capital, eft_tags=symbols, fdir=self.fdir)

        p.load()

        optimizer = self.fac.create(enums.OptimizerType[method.upper()], portfolio=p)
        optimizer.optimize_portfolio()
        p.calc_historical_returns()
        return p
    def post(self, request):
        input_serializer = self.input_serializer_method(data=request.data)
        if input_serializer.is_valid():

            p = self.generate_porfolio(input_serializer)
            analyzer = Analyzer(p, rank_file_path=self.rpath, comments_output_path=self.cpath)
            history = analyzer.history()
            df_target=  analyzer.analyze()
            df_target = df_target.drop(columns=['positive_comp', 'negative_comp', 'benchmark_name', 'benchmark_name_2','累计净值'])
            df_target.fillna(0, inplace=True)
            df_target.replace([np.inf, -np.inf], 0, inplace=True)
            analyses = []
            scores = []
            score_pairs = {
                "vol": "stock_volatility_benchmark.csv",
                "drawdown_amount": "stock_drawdown_amount_benchmark.csv",
                "beta": "stock_positive_beta_benchmark.csv",
                "alpha": "stock_alpha_benchmark.csv",
                "rolling_SR": "stock_rolling_sharpe_benchmark.csv",
                "annual_return": "stock_return_benchmark.csv",
            }
            for col in df_target.columns:
                values = [{"date": date.strftime('%Y-%m-%d'), "value": value} for date, value in zip(df_target.index, df_target[col])]
                analyses.append({"type":col, "values":values})

            for name, file in score_pairs.items():
                score = self.score_pair[name](df_target, name, file)
                scores.append({"type":name, "value": score})

            response_data = {
                "portfolio": {
                    "component": p.weights,
                    "returns": history
                },
                "analysis": analyses,
                "score": scores,
            }
            output_serializer = AnalyzerOutputSerializer(response_data)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FundRankView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fdir = settings.RETURNS_DATA_FILE_PATH
        self.rpath = settings.RANK_FILE_PATH
        self.cpath = settings.COMMENTS_FILE_PATH
        self.pairs = {
            "vol": "stock_volatility_benchmark.csv",
            "drawdown_amount": "stock_drawdown_amount_benchmark.csv",
            "beta": "stock_positive_beta_benchmark.csv",
            "alpha": "stock_alpha_benchmark.csv",
            "rolling_SR": "stock_rolling_sharpe_benchmark.csv",
            "annual_return": "stock_return_benchmark.csv",
        }
        self.order_func = {
            "vol": self._ascend,
            "drawdown_amount": self._ascend,
            "beta": self._ascend,
            "alpha": self._descend,
            "rolling_SR": self._descend,
            "annual_return": self._descend,
        }

    def _ascend(self, df):
        df = df.nsmallest(10, 'value')
        return df['ticker']

    def _descend(self, df):
        df = df.nlargest(10, 'value')
        return df['ticker']

    def get(self, request):
        metric = request.query_params.get('metric')

        file = self.pairs[metric]
        if self.fdir is None:
            self.fdir = "D:/workspace/aggregation/"
        if self.rpath is None:
            self.rpath = "D:/workspace/output_search/"
        if self.cpath is None:
            self.cpath = "D:/workspace/comments/"
        fpath = os.path.join(self.rpath, file)
        tickers = list(self.order_func[metric](pd.read_csv(fpath)))

        return Response(tickers)


class CustomPortfolioView(OptimizePortfolioView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fdir = settings.RETURNS_DATA_FILE_PATH
        self.rpath = settings.RANK_FILE_PATH
        self.cpath = settings.COMMENTS_FILE_PATH
        self.fac = OptimizerFactory()
        self.score_pair = {
            "vol": self._reverse_score,
            "drawdown_amount": self._reverse_score,
            "beta": self._reverse_score,
            "alpha": self._score,
            "rolling_SR": self._score,
            "annual_return": self._score,
        }
        self.input_serializer_method = CustomInputSerializer
    def generate_porfolio(self, input_serializer):
        capital = input_serializer.validated_data['amount']
        weights = input_serializer.validated_data['weights']
        if self.fdir is None:
            self.fdir = "D:/workspace/aggregation/"
        if self.rpath is None:
            self.rpath = "D:/workspace/output_search/"
        if self.cpath is None:
            self.cpath = "D:/workspace/comments/"

        symbols = [ w["symbol"] for w in weights ]
        p = Portfolio(capital, eft_tags=symbols, fdir=self.fdir)
        p.load()
        p.weights = [ {"fund": weight["symbol"], "weight":weight["weight"], "amount":weight["weight"]*capital} for weight in weights]
        p.calc_historical_returns()
        return p


class DefaultPortfolioView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fdir = "/home/app/Desktop/default_portfolio/default_portfolio.json"

    def get(self, request):
        with open(self.fdir, 'r') as file:
            response_data = json.load(file)

        output_serializer = AnalyzerOutputSerializer(response_data)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class TimingPortfolioView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ret_file = home + "/Desktop/default_portfolio/timing.csv"
        # self.ret_file = "D:/workspace/timing/timing.csv"

    def get(self, request):
        df = pd.read_csv(self.ret_file)
        json_return = df.to_json(orient="records")
        return Response(json.loads(json_return), status=status.HTTP_200_OK)










