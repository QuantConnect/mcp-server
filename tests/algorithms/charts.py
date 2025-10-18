# ruff: noqa: F403, F405
# region imports
from AlgorithmImports import *
# endregion


class ChartTestAlgorithm(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2023, 1, 1)
        self.set_end_date(2023, 4, 1)
        symbol = self.add_equity("SPY", Resolution.DAILY).symbol
        self.plot_indicator("SMA", self.sma(symbol, 10))
