
import unittest
import time
from main import ChronosMatch


class TestBenchmark(unittest.TestCase):

    def test_engine_accepts_many_orders(self):
        engine = ChronosMatch()
        start = time.perf_counter()

        for order_id in range(1000):
            engine.add_buy_order(order_id, 100.0, 1)

        elapsed = time.perf_counter() - start

        self.assertEqual(len(engine.buy_orders), 1000)
        self.assertGreater(elapsed, 0)

        print(f"\nAdded 1000 orders in {elapsed:.6f} seconds")


if __name__ == "__main__":
    unittest.main()
