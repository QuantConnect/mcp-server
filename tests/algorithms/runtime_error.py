# ruff: noqa: F403, F405
# region imports
from AlgorithmImports import *
# endregion


class BacktestRuntimeErrorTestAlgorithm(QCAlgorithm):

    def initialize(self):
        raise Exception('Test')
