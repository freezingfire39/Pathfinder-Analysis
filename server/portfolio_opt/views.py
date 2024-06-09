from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from portfolio.factory import OptimizerFactory
from portfolio.portfolio_ import Portfolio
from portfolio.utils import enums
from .serializers import OptimizationInputSerializer, OptimizedPortfolioSerializer
import numpy as np
from scipy.optimize import minimize


class OptimizePortfolioView(APIView):
    fdir = "D:/workspace/Pathfinder-Analysis/sample"
    fac = OptimizerFactory()
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

            output_serializer = OptimizedPortfolioSerializer(p.weights, many=True)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
