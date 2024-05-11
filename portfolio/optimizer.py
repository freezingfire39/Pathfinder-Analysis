from abc import ABC, abstractmethod

from portfolio.portfolio import Portfolio


class PortfolioOptimizer(ABC):

    def __init__(self, capital):
        self.capital = capital
    @abstractmethod
    def optimize_portfolio(self, portfolio: Portfolio):
        pass

class EquallyWeightedOptimizer(PortfolioOptimizer):
    def __init__(self, capital):
        super().__init__(capital)

    def optimize_portfolio(self, portfolio: Portfolio):
        # Implement equally weighted optimization logic
        return {key:self.capital/portfolio.get_size() for key in portfolio.get_funds().keys()}

class MinimalVolatilityOptimizer(PortfolioOptimizer):
    def optimize_portfolio(self, portfolio):
        # Implement minimal volatility optimization logic
        pass

class MaxSharpeRatioOptimizer(PortfolioOptimizer):
    def optimize_portfolio(self, portfolio):
        # Implement max Sharpe ratio optimization logic
        pass