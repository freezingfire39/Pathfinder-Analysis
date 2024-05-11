import utils.enums
import os
from typing import List
import pandas as pd

class Fund:
    def __init__(self, name: str):
        self.name = name
        self.background = None
        self.holdings = None
        self.prices = None
        self.industry = None

    def __repr__(self):
        pass

    def load(self, directory: str):
        self.background = pd.read_csv(os.path.join(directory, 'Background.csv'))
        self.holdings = pd.read_csv(os.path.join(directory, 'Holdings.csv'))
        self.prices = pd.read_csv(os.path.join(directory, 'Fund_1.csv'))
        self.industry = pd.read_csv(os.path.join(directory, 'Industry.csv'))


class Portfolio:

    def __init__(self, amount: float, eft_tags: List[str], fdir: str):
        self.tot_amount = amount
        self.etf_symbols = eft_tags
        self.fdir = fdir
        self._portfolio = dict()
        self._size = 0

    def is_valid(self) -> bool:
        return self._is_valid_symbol() and self._is_valid_amount()

    def _is_valid_symbol(self) -> bool:

        for tag in self.etf_symbols:
            symbol_path = os.path.join(self.fdir, tag)
            if not os.path.isdir(symbol_path):
                return False

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
            self._portfolio[symbol] = fund

    def get_portfolio(self) -> dict:
        return self._portfolio

    def get_size(self) -> int:
        return self._size