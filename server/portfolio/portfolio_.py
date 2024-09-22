import numpy as np

import portfolio.utils.enums
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

    def load(self, directory: str):
        # self._load_background(directory)
        # self._load_holdings(directory)
        self._load_returns(directory)
        # self._load_industry(directory)

    def _load_background(self, directory: str):
        self.background = pd.read_csv(os.path.join(directory, self.name, 'Background.csv'))

    def _load_holdings(self, directory: str):
        self.holdings = pd.read_csv(os.path.join(directory, self.name, 'Holdings.csv'))

    def _load_industry(self, directory: str):
        self.industry = pd.read_csv(os.path.join(directory, self.name, 'Industry.csv'))

    def _load_returns(self, directory: str):
        prices = pd.read_csv(os.path.join(directory, self.name, 'sample_feature.csv'))
        prices["date"] = prices["净值日期"]
        prices["date"] = pd.to_datetime(prices["date"])
        prices.set_index("date",inplace=True)
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
        self._weights = list()
        self.returns = pd.DataFrame()

    def __repr__(self):
        return json.dumps(self._weights)

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

    @property
    def funds(self) -> dict[str, Fund]:
        return self._funds

    @property
    def size(self):
        return self._size

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, weights: dict[str, float]):
        self._weights = weights


    def _calculate_returns(self):
        merged_df = None
        for symbol in self.etf_symbols:
            sym_return = self.funds[symbol].get_returns()
            if merged_df is None:
                merged_df = sym_return.rename(columns={'return': symbol})
            else:
                merged_df = merged_df.join(sym_return.rename(columns={'return': symbol}), how='outer')

        return merged_df.dropna()

    def calc_historical_returns(self):
        if len(self.weights) == 0:
            return
        weight_vector = np.array([ item["weight"] for item in self._weights])
        returns = self._calculate_returns().dot((weight_vector.reshape(-1, 1)))
        self.returns = returns.rename(columns={0:"return"})



if __name__ == '__main__':
    from portfolio.factory import OptimizerFactory
    from portfolio.optimizer import PortfolioOptimizer, EquallyWeightedOptimizer, MinimalVolatilityOptimizer, \
        MaxSharpeRatioOptimizer
    fac = OptimizerFactory()
    fdir = "D:/workspace/Pathfinder-Analysis/sample"
    p = Portfolio(1e6, eft_tags=['000001','000003'],fdir=fdir)
    p.load()