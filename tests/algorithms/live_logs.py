# ruff: noqa: F403, F405
# region imports
from AlgorithmImports import *
# endregion


class LiveLogTestAlgorithm(QCAlgorithm):

    def initialize(self):
        for i in range(10):
            self.log(f'Log test {i}')
