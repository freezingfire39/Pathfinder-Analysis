from abc import ABC, abstractmethod

class PortfolioOptimizer(ABC):
    @abstractmethod
    def optimize_portfolio(self, portfolio):
        pass

class EquallyWeightedOptimizer(PortfolioOptimizer):
    def optimize_portfolio(self, portfolio):
        # Implement equally weighted optimization logic
        pass

class MinimalVolatilityOptimizer(PortfolioOptimizer):
    def optimize_portfolio(self, portfolio):
        # Implement minimal volatility optimization logic
        pass

class MaxSharpeRatioOptimizer(PortfolioOptimizer):
    def optimize_portfolio(self, portfolio):
        # Implement max Sharpe ratio optimization logic
        pass