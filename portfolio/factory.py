from portfolio.optimizer import EquallyWeightedOptimizer, MinimalVolatilityOptimizer, MaxSharpeRatioOptimizer
from portfolio.utils.enums import OptimizerType


class OptimizerFactory(object):

    def __init__(self):
        self._optimizers = {}

    def register_optimizer(self, key, builder):
        self._optimizers[key] = builder

    def create(self, key, **kwargs):
        builder = self._optimizers.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)


if __name__ == '__main__':
    fac = OptimizerFactory()
    fac.register_optimizer(OptimizerType.EQUAL_WEIGHT, EquallyWeightedOptimizer)
    fac.register_optimizer(OptimizerType.MIN_VOLATILITY, MinimalVolatilityOptimizer)
    fac.register_optimizer(OptimizerType.MAX_SHARPE_RATIO, MaxSharpeRatioOptimizer)

