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
from .serializers import OptimizationInputSerializer, OptimizedPortfolioSerializer, AnalyzerOutputSerializer
import numpy as np
from scipy.optimize import minimize
from django.conf import settings
from portfolio.analyzer import Analyzer


class OptimizePortfolioView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fdir = settings.RETURNS_DATA_FILE_PATH
        self.rpath = settings.RANK_FILE_PATH
        self.cpath = settings.COMMENTS_FILE_PATH
        self.fac = OptimizerFactory()

    def score(self, df, col, file):
        p_value = df[col].iloc[-1]
        fpath = os.path.join(self.rpath, file)
        df = pd.read_csv(fpath)
        score = percentileofscore(df["value"].dropna().to_list(), p_value)
        return score

    def post(self, request):
        input_serializer = OptimizationInputSerializer(data=request.data)
        if input_serializer.is_valid():
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
                score = self.score(df_target, name, file)
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


