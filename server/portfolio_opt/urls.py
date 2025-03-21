from django.urls import path
from .views import OptimizePortfolioView, FundRankView, CustomPortfolioView, DefaultPortfolioView

urlpatterns = [
    path('api/v1/py/analysis/', OptimizePortfolioView.as_view(), name='analyze portfolio'),
    path('api/v1/py/custom/portfolio/', CustomPortfolioView.as_view(), name='customized portfolio'),
    path('api/v1/py/rank/', FundRankView.as_view(), name='rank portfolio'),
    path('api/v1/py/default/portfolio/', DefaultPortfolioView.as_view(), name='default portfolio'),
]