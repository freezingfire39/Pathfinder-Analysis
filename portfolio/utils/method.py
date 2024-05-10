from enum import Enum


class Method(Enum):
    EQUAL_WEIGHT = 1
    MIN_VOLATILITY = 2
    MAX_SHARPE_RATIO = 3
    