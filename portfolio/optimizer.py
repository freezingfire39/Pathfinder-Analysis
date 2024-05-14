from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from portfolio.portfolio_ import Portfolio

class PortfolioOptimizer(ABC):

    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio
    @abstractmethod
    def optimize_portfolio(self):
        pass

    def _calculate_returns(self):
        merged_df = None
        for symbol in self.portfolio.etf_symbols:
            sym_return = self.portfolio.get_funds()[symbol].get_returns()
            if merged_df is None:
                merged_df = sym_return.rename(columns={'return': symbol})
            else:
                merged_df = merged_df.join(sym_return.rename(columns={'return': symbol}), how='outer')

        return merged_df

class EquallyWeightedOptimizer(PortfolioOptimizer):

    def optimize_portfolio(self):
        # Implement equally weighted optimization logic
        return {key:self.portfolio.tot_amount/self.portfolio.get_size() for key in self.portfolio.get_funds().keys()}

class MinimalVolatilityOptimizer(PortfolioOptimizer):
    def optimize_portfolio(self):
        # Implement minimal volatility optimization logic
        num_funds = self.portfolio.get_size()
        initial_allocation = np.ones(num_funds) / num_funds  # Equal allocation initially
        returns =self._calculate_returns()
        returns.dropna(inplace=True)
        # Calculate covariance matrix of returns
        cov_matrix = np.cov(returns, rowvar=False)

        # Define objective function to minimize portfolio volatility
        def portfolio_volatility(weights):
            portfolio_return = np.dot(weights, np.mean(returns, axis=0))
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            return portfolio_volatility

        # constraints: weights sum to 1
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        # weights: 0 <= weights <= 1
        bounds = tuple((0, 1) for _ in range(num_funds))
        optimized_weights = minimize(portfolio_volatility, initial_allocation, method='SLSQP', bounds=bounds,
                                     constraints=constraints).x

        allocated_money = self.portfolio.tot_amount * optimized_weights

        weights = { num_funds[i]: allocated_money[i]  for i in range(num_funds)}
        self.portfolio.set_weights(weights)

class MaxSharpeRatioOptimizer(PortfolioOptimizer):
    def __init__(self, portfolio: Portfolio, risk_free_rate=0.0):
        super().__init__(portfolio)
        self._risk_free_rate = risk_free_rate

    def optimize_portfolio(self):
        # check funds 1 year history
        num_funds = self.portfolio.get_size()
        returns = self._calculate_returns()

        initial_allocation = np.ones(num_funds) / num_funds  # Equal allocation initially

        mean_returns = np.mean(returns, axis=0)
        cov_matrix = np.cov(returns, rowvar=False)

        def negative_sharpe_ratio(weights):
            portfolio_return = np.dot(weights, mean_returns)
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            sharpe_ratio = (portfolio_return - self._risk_free_rate) / portfolio_volatility
            return -sharpe_ratio

        # constraints: weights sum to 1
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

        # bounds for weights: 0 <= weights <= 1
        bounds = tuple((0, 1) for _ in range(num_funds))
        optimized_weights = minimize(negative_sharpe_ratio, initial_allocation, method='SLSQP', bounds=bounds, constraints=constraints).x

        allocated_money = self.portfolio.tot_amount * optimized_weights
        weights = {num_funds[i]: allocated_money[i] for i in range(num_funds)}
        self.portfolio.set_weights(weights)


if __name__ == '__main__':
    from factory import OptimizerFactory

    from portfolio.utils import enums
    fac = OptimizerFactory()
    fac.register_optimizer(enums.OptimizerType.EQUAL_WEIGHT, EquallyWeightedOptimizer)
    fac.register_optimizer(enums.OptimizerType.MIN_VOLATILITY, MinimalVolatilityOptimizer)
    fac.register_optimizer(enums.OptimizerType.MAX_SHARPE_RATIO, MaxSharpeRatioOptimizer)
    fdir = "D:/workspace/Pathfinder-Analysis/sample"
    p = Portfolio(1e6, eft_tags=['000001','000003'],fdir=fdir)
    p.load()

    optimizer = fac.create(enums.OptimizerType.MIN_VOLATILITY, portfolio=p)
    optimizer.optimize_portfolio()

