# ruff: noqa: F403, F405
# region imports
from AlgorithmImports import *
# endregion


class InsightTestAlgorithm(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2024, 1, 8)
        self.set_end_date(2024, 4, 1)
        self.set_cash(100000)
        self.add_equity("SPY", Resolution.DAILY)
        self.add_alpha(
            ConstantAlphaModel(
                InsightType.PRICE, InsightDirection.UP, timedelta(30), 
                0.1, 0.2, 0.3
            )
        )
        self.set_portfolio_construction(EqualWeightingPortfolioConstructionModel())
