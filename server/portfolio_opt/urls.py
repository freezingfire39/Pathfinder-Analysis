from django.urls import path
from .views import OptimizePortfolioView

urlpatterns = [
    path('api/v1/py/analysis/', OptimizePortfolioView.as_view(), name='analyze portfolio'),
]