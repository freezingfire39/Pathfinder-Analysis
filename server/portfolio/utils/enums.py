from enum import Enum


class OptimizerType(Enum):
    EQUALLY_WEIGHTED = 1
    MIN_VOLATILITY = 2
    MAX_SHARPE_RATIO = 3
    