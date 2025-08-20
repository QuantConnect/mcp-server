# region imports
from AlgorithmImports import *
# endregion


class BacktestRuntimeErrorTestAlgorithm(QCAlgorithm):

    def initialize(self):
        raise Exception('Test')