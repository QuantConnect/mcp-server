# ruff: noqa: F403, F405
from AlgorithmImports import *


class UpdateCodeToPEP8TestAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.AddEquity('SPY')
