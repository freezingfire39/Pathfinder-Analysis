from django.urls import path
from .views import OptimizePortfolioView

urlpatterns = [
    path('optimize/', OptimizePortfolioView.as_view(), name='optimize portfolio'),
]