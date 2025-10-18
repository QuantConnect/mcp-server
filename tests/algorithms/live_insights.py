# ruff: noqa: F403, F405
# region imports
from AlgorithmImports import *
# endregion


class LiveInsightsTestAlgorithm(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2025, 7, 10)
        self._insights = 0
        self._symbol = self.add_crypto('BTCUSD', Resolution.SECOND).symbol
        self.set_portfolio_construction(
            EqualWeightingPortfolioConstructionModel()
        )

    def on_data(self, data: Slice):
        # Only emit 10 insights.
        if self._insights >= 10:
            return
        self._insights += 1
        # Determine the direction.
        if self.portfolio.invested:
            direction = InsightDirection.FLAT
        else:
            direction = InsightDirection.UP
        # Emit the insight.
        self.emit_insights(
            Insight.price(self._symbol, timedelta(1), direction)
        )
