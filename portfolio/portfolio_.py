import utils.enums
import os
from typing import List
import pandas as pd
import json

class Fund:
    def __init__(self, name: str):
        self.name = name
        self.background = None
        self.holdings = None
        self.returns = None
        self.industry = None

    def __repr__(self):
        pass

    def load(self, directory: str):
        self._load_background(directory)
        # self._load_holdings(directory)
        self._load_returns(directory)
        self._load_industry(directory)

    def _load_background(self, directory: str):
        self.background = pd.read_csv(os.path.join(directory, self.name, 'Background.csv'))

    def _load_holdings(self, directory: str):
        self.holdings = pd.read_csv(os.path.join(directory, self.name, 'Holdings.csv'))

    def _load_industry(self, directory: str):
        self.industry = pd.read_csv(os.path.join(directory, self.name, 'Industry.csv'))

    def _load_returns(self, directory: str):
        prices = pd.read_csv(os.path.join(directory, self.name, 'Fund_1.csv'))
        prices["date"] = prices["净值日期"]
        prices["date"] = pd.to_datetime(prices["date"])
        prices.set_index("date",inplace=True)
        prices = prices.loc[prices.iloc[:,3]!='封闭期']
        prices["return"] = prices.iloc[:, 1].pct_change()
        self.returns = prices["return"].reset_index().set_index('date')

    def get_returns(self):
        return self.returns

class Portfolio:

    def __init__(self, amount: float, eft_tags: List[str], fdir: str):
        self.tot_amount = amount
        self.etf_symbols = eft_tags
        self.fdir = fdir
        self._funds = dict()
        self._size = 0
        self._weights = dict()

    def __repr__(self):
        return json.dumps(self.portfolio.weights)

    def is_valid(self) -> bool:
        return self._is_valid_symbol() and self._is_valid_amount()

    def _is_valid_symbol(self) -> bool:

        for tag in self.etf_symbols:
            symbol_path = os.path.join(self.fdir, tag)
            if not os.path.isdir(symbol_path):
                return False

        # symbol open/closed
        return True
    def _is_valid_amount(self) -> bool:
        return self.tot_amount > 0

    def read_symbol(self, symbol: str) -> Fund:
        return Fund(symbol)

    def load(self):
        self._size = len(self.etf_symbols)
        for symbol in self.etf_symbols:
            fund = self.read_symbol(symbol)
            fund.load(self.fdir)
            self._funds[symbol] = fund

    def get_funds(self) -> dict[str, Fund]:
        return self._funds

    def get_size(self) -> int:
        return self._size

    def set_weights(self, weights: dict[str, float]):
        self.weights = weights


if __name__ == '__main__':
    from portfolio.factory import OptimizerFactory
    from portfolio.optimizer import PortfolioOptimizer, EquallyWeightedOptimizer, MinimalVolatilityOptimizer, \
        MaxSharpeRatioOptimizer
    fac = OptimizerFactory()
    fac.register_optimizer(utils.enums.OptimizerType.EQUAL_WEIGHT, EquallyWeightedOptimizer)
    fac.register_optimizer(utils.enums.OptimizerType.MIN_VOLATILITY, MinimalVolatilityOptimizer)
    fac.register_optimizer(utils.enums.OptimizerType.MAX_SHARPE_RATIO, MaxSharpeRatioOptimizer)
    fdir = "D:/workspace/Pathfinder-Analysis/sample"
    p = Portfolio(1e6, eft_tags=['000001','000003'],fdir=fdir)
    p.load()