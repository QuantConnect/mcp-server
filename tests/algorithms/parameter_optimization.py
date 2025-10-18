# ruff: noqa: F403, F405
# region imports
from AlgorithmImports import *
# endregion


class ParameterOptimizationTestAlgorithm(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2010, 1, 1)
        self.set_end_date(2025, 1, 1)
        self._equity = self.add_equity("SPY", Resolution.DAILY)
        self.settings.automatic_indicator_warm_up = True
        self._sma_slow = self.sma(
            self._equity.symbol, self.get_parameter('sma_slow', 21)
        )
        self._sma_fast = self.sma(
            self._equity.symbol, self.get_parameter('sma_fast', 5)
        )

    def on_data(self, data: Slice):
        if (not self._equity.holdings.is_long and 
            self._sma_fast > self._sma_slow):
            self.set_holdings(self._equity.symbol, 1)
            return
        if (not self._equity.holdings.is_short and 
            self._sma_fast < self._sma_slow):
            self.set_holdings(self._equity.symbol, -1)
