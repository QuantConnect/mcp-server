# ruff: noqa: F403, F405
# region imports
from AlgorithmImports import *
# endregion


class LiveLiquidateTestAlgorithm(QCAlgorithm):

    def initialize(self):
        # Add BTCUSD, which trades 24/7, so the algorithm can fill
        # liquidation orders whenever we run the test suite.
        self.add_crypto("BTCUSD", Resolution.SECOND)
