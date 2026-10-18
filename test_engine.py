
import unittest
from main import ChronosMatch


class TestChronosMatch(unittest.TestCase):

    def test_matching_orders(self):
        engine = ChronosMatch()

        engine.add_buy_order(1, 105, 10)
        engine.add_sell_order(2, 100, 5)

        self.assertEqual(len(engine.buy_orders), 1)
        self.assertEqual(engine.buy_orders[0]["quantity"], 5)
        self.assertEqual(len(engine.sell_orders), 0)

    def test_no_match_when_prices_do_not_cross(self):
        engine = ChronosMatch()

        engine.add_buy_order(1, 95, 10)
        engine.add_sell_order(2, 100, 5)

        self.assertEqual(len(engine.buy_orders), 1)
        self.assertEqual(len(engine.sell_orders), 1)


if __name__ == "__main__":
    unittest.main()
