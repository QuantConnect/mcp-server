# ruff: noqa: F403, F405
# region imports
from AlgorithmImports import *
# endregion


class OrderPropertiesTestAlgorithm(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2024, 1, 8)
        self.set_end_date(2024, 2, 1)
        self.set_cash(100_000)
        self._equity = self.add_equity(
            'SPY', Resolution.HOUR, 
            data_normalization_mode=DataNormalizationMode.RAW
        )
        
    def on_data(self, data: Slice):
        if self.portfolio.invested:
            return
        tag = 'some tag'
        quantity = 1
        limit_price = self._equity.price + 10
        # Test the GOOD_TIL_CANCELED time in force.
        order_properties = OrderProperties()
        order_properties.time_in_force = TimeInForce.GOOD_TIL_CANCELED
        self.limit_order(
            self._equity.symbol, quantity, limit_price, tag, order_properties
        )

        # Test the Day time in force.
        order_properties = OrderProperties()
        order_properties.time_in_force = TimeInForce.DAY
        self.limit_order(
            self._equity.symbol, quantity, limit_price, tag, order_properties
        )

        # Test the good_til_date time in force.
        order_properties = OrderProperties()
        order_properties.time_in_force = TimeInForce.good_til_date(
            datetime(2025, 1, 1)
        )
        self.limit_order(
            self._equity.symbol, quantity, limit_price, tag, order_properties
        )
