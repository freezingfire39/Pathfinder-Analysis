from portfolio.optimizer import PortfolioOptimizer


class OptimizerFactory(object):

    def __init__(self):
        self._optimizers = {}

    def register_optimizer(self, key, builder):
        self._optimizers[key] = builder

    def create(self, key, **kwargs)->PortfolioOptimizer:
        builder = self._optimizers.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)


