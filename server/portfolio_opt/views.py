import os

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
        self.fac = OptimizerFactory()
    def post(self, request):
        input_serializer = OptimizationInputSerializer(data=request.data)
        if input_serializer.is_valid():
            symbols = input_serializer.validated_data['symbols']
            capital = input_serializer.validated_data['amount']
            method = input_serializer.validated_data['method']

            p = Portfolio(capital, eft_tags=symbols, fdir=self.fdir)

            p.load()

            optimizer = self.fac.create(enums.OptimizerType[method.upper()], portfolio=p)
            optimizer.optimize_portfolio()
            p.calc_historical_returns()
            analyzer = Analyzer(p)
            history = analyzer.history()
            rolling_sr=  analyzer.rolling_sharpe()
            rolling_vol = analyzer.rolling_volatility()
            max_dd = analyzer.max_drawdown()

            response_data = {
                "portfolio": {
                    "component": p.weights,
                    "returns": history
                },
                "analysis": [
                    {"type": "rolling_sharpe","values":rolling_sr[0], "comment": rolling_sr[1]},
                    {"type": "rolling_vol", "values": rolling_vol[0], "comment": rolling_vol[1]},
                    {"type": "max_drawdown", "values": max_dd[0], "comment":max_dd[1]},
                ]
            }
            output_serializer = AnalyzerOutputSerializer(response_data)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
