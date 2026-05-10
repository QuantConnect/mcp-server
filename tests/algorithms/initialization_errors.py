# ruff: noqa: F403, F405
from AlgorithmImports import *


class BacktestInitTestAlgorithm(QCAlgorithm):

    def initialize(self):
        self.add_equity('SPY', Resolution.DAY)
