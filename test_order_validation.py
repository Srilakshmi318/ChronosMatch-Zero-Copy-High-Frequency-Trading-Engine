
import unittest
from main import ChronosMatch


class TestOrderValidation(unittest.TestCase):

    def setUp(self):
        self.engine = ChronosMatch()

    def test_buy_order_is_added(self):
        self.engine.add_buy_order(1, 100.0, 10)

        self.assertEqual(len(self.engine.buy_orders), 1)
        self.assertEqual(self.engine.buy_orders[0]["quantity"], 10)

    def test_sell_order_is_added(self):
        self.engine.add_sell_order(2, 101.0, 5)

        self.assertEqual(len(self.engine.sell_orders), 1)
        self.assertEqual(self.engine.sell_orders[0]["quantity"], 5)

    def test_matching_reduces_remaining_quantity(self):
        self.engine.add_buy_order(1, 105.0, 10)
        self.engine.add_sell_order(2, 100.0, 5)

        self.assertEqual(self.engine.buy_orders[0]["quantity"], 5)
        self.assertEqual(len(self.engine.sell_orders), 0)


if __name__ == "__main__":
    unittest.main()
