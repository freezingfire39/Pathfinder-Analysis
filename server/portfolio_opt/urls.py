from django.urls import path
from .views import OptimizePortfolioView, FundRankView

urlpatterns = [
    path('api/v1/py/analysis/', OptimizePortfolioView.as_view(), name='analyze portfolio'),
    path('api/v1/py/rank/', FundRankView.as_view(), name='rank portfolio'),
]