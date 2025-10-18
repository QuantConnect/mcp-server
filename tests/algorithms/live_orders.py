# ruff: noqa: F403, F405
# region imports
from AlgorithmImports import *
# endregion


class LiveOrdersTestAlgorithm(QCAlgorithm):

    def initialize(self):
        self._trades = 0
        self._btc = self.add_crypto('BTCUSD', Resolution.SECOND)

    def on_data(self, data: Slice):
        if self._trades >= 10:
            return
        self._trades += 1
        self.set_holdings(self._btc.symbol, 0 if self.portfolio.invested else 1)
