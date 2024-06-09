from portfolio.optimizer import PortfolioOptimizer, EquallyWeightedOptimizer, MinimalVolatilityOptimizer, \
    MaxSharpeRatioOptimizer
from portfolio.utils import enums


class OptimizerFactory(object):

    def __init__(self):
        self._optimizers = {}
        self._register_optimizer(enums.OptimizerType.EQUALLY_WEIGHTED, EquallyWeightedOptimizer)
        self._register_optimizer(enums.OptimizerType.MIN_VOLATILITY, MinimalVolatilityOptimizer)
        self._register_optimizer(enums.OptimizerType.MAX_SHARPE_RATIO, MaxSharpeRatioOptimizer)

    def _register_optimizer(self, key, builder):
        self._optimizers[key] = builder

    def create(self, key, **kwargs)->PortfolioOptimizer:
        builder = self._optimizers.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)


