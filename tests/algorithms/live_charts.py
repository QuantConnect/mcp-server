# ruff: noqa: F403, F405
# region imports
from AlgorithmImports import *
# endregion


class LiveChartTestAlgorithm(QCAlgorithm):

    def initialize(self):
        symbol = self.add_crypto("BTCUSD", Resolution.SECOND).symbol
        self.plot_indicator("SMA", self.sma(symbol, 10))
