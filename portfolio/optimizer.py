from abc import ABC, abstractmethod
import numpy as np
from scipy.optimize import minimize
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
    def optimize_portfolio(self, funds):
        # Implement minimal volatility optimization logic
        num_funds = len(funds)
        initial_allocation = np.ones(num_funds) / num_funds  # Equal allocation initially
        returns =self._calculate_returns(funds)
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

        allocated_money = self.capital * optimized_weights

        return list(zip(funds, allocated_money))

    def _calculate_returns(self, funds):
        pass

class MaxSharpeRatioOptimizer(PortfolioOptimizer):
    def __init__(self, capital, funds_data, risk_free_rate=0.0):
        super().__init__(capital)
        self._funds_data = funds_data
        self._risk_free_rate = risk_free_rate

    def optimize_portfolio(self, funds):
        num_funds = len(funds)
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

        allocated_money = self.capital * optimized_weights

        return list(zip(funds, allocated_money))

    def _calculate_returns(self):
        pass
