
import unittest
from main import ChronosMatch


class TestWeek3(unittest.TestCase):

    def setUp(self):
        self.engine = ChronosMatch()

    def test_buy_order(self):
        self.engine.add_buy_order(1, 100, 10)
        self.assertEqual(len(self.engine.buy_orders), 1)

    def test_sell_order(self):
        self.engine.add_sell_order(2, 105, 5)
        self.assertEqual(len(self.engine.sell_orders), 1)

    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            self.engine.add_buy_order(1, -100, 5)

    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.engine.add_buy_order(1, 100, 0)

    def test_invalid_order_id(self):
        with self.assertRaises(ValueError):
            self.engine.add_buy_order(-1, 100, 5)

    def test_duplicate_order_id(self):
        self.engine.add_buy_order(1, 100, 5)
        with self.assertRaises(ValueError):
            self.engine.add_sell_order(1, 100, 5)

    def test_no_match(self):
        self.engine.add_buy_order(1, 95, 10)
        self.engine.add_sell_order(2, 100, 5)
        self.assertEqual(len(self.engine.trade_history), 0)

    def test_complete_matching(self):
        self.engine.add_buy_order(1, 110, 10)
        self.engine.add_sell_order(2, 100, 10)
        self.assertEqual(len(self.engine.trade_history), 1)
        self.assertEqual(len(self.engine.buy_orders), 0)
        self.assertEqual(len(self.engine.sell_orders), 0)

    def test_partial_execution(self):
        self.engine.add_buy_order(1, 105, 10)
        self.engine.add_sell_order(2, 100, 4)
        self.assertEqual(self.engine.buy_orders[0]["quantity"], 6)
        self.assertEqual(len(self.engine.sell_orders), 0)

    def test_price_priority(self):
        self.engine.add_buy_order(1, 100, 5)
        self.engine.add_buy_order(2, 105, 5)
        trades = self.engine.add_sell_order(3, 99, 5)
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]["buy_order_id"], 2)

    def test_time_priority(self):
        self.engine.add_buy_order(1, 100, 5)
        self.engine.add_buy_order(2, 100, 5)
        self.assertEqual(self.engine.buy_orders[0]["id"], 1)

    def test_order_cancellation(self):
        self.engine.add_buy_order(1, 100, 5)
        self.assertTrue(self.engine.cancel_order(1))
        self.assertEqual(len(self.engine.buy_orders), 0)

    def test_cancel_missing_order(self):
        self.assertFalse(self.engine.cancel_order(999))

    def test_trade_history(self):
        self.engine.add_buy_order(1, 105, 10)
        self.engine.add_sell_order(2, 100, 5)
        self.assertEqual(len(self.engine.trade_history), 1)
        self.assertEqual(self.engine.trade_history[0]["quantity"], 5)

    def test_order_book_snapshot(self):
        self.engine.add_buy_order(1, 100, 5)
        snapshot = self.engine.get_order_book()
        self.assertEqual(len(snapshot["buy_orders"]), 1)
        self.assertEqual(snapshot["buy_orders"][0]["id"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
