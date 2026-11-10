
import os
import tempfile
import unittest

from ring_buffer import RingBuffer


class TestRingBuffer(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filename = os.path.join(
            self.temp_dir.name, "test_orders.bin"
        )
        self.buffer = RingBuffer(
            filename=self.filename, capacity=4
        )

    def tearDown(self):
        self.buffer.close()
        self.temp_dir.cleanup()

    def test_write_and_read_buy_order(self):
        self.assertTrue(
            self.buffer.write(1, "B", 150.25, 10)
        )
        order = self.buffer.read()

        self.assertEqual(order["order_id"], 1)
        self.assertEqual(order["side"], "BUY")
        self.assertEqual(order["price"], 150.25)
        self.assertEqual(order["quantity"], 10)

    def test_write_and_read_sell_order(self):
        self.assertTrue(
            self.buffer.write(2, "S", 200.50, 5)
        )
        order = self.buffer.read()

        self.assertEqual(order["side"], "SELL")
        self.assertEqual(order["price"], 200.50)

    def test_empty_buffer(self):
        self.assertIsNone(self.buffer.read())

    def test_buffer_full(self):
        self.assertTrue(self.buffer.write(1, "B", 100, 1))
        self.assertTrue(self.buffer.write(2, "S", 101, 1))
        self.assertTrue(self.buffer.write(3, "B", 102, 1))

        self.assertFalse(
            self.buffer.write(4, "S", 103, 1)
        )

    def test_fifo_order(self):
        for order_id in range(3):
            self.buffer.write(order_id, "B", 100, 1)

        for expected_id in range(3):
            order = self.buffer.read()
            self.assertEqual(order["order_id"], expected_id)

    def test_buffer_wraparound(self):
        for order_id in range(3):
            self.buffer.write(order_id, "B", 100, 1)

        self.buffer.read()
        self.buffer.read()

        self.assertTrue(self.buffer.write(3, "S", 101, 1))
        self.assertTrue(self.buffer.write(4, "S", 102, 1))

        self.assertEqual(self.buffer.read()["order_id"], 2)
        self.assertEqual(self.buffer.read()["order_id"], 3)
        self.assertEqual(self.buffer.read()["order_id"], 4)

    def test_invalid_order_id(self):
        with self.assertRaises(ValueError):
            self.buffer.write(-1, "B", 100, 1)

    def test_invalid_side(self):
        with self.assertRaises(ValueError):
            self.buffer.write(1, "X", 100, 1)

    def test_invalid_price(self):
        for price in [0, -10, float("inf"), float("nan")]:
            with self.subTest(price=price):
                with self.assertRaises(ValueError):
                    self.buffer.write(1, "B", price, 1)

    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.buffer.write(1, "B", 100, 0)

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            RingBuffer(
                filename=os.path.join(
                    self.temp_dir.name, "invalid.bin"
                ),
                capacity=1
            )

    def test_context_manager(self):
        filename = os.path.join(
            self.temp_dir.name, "context.bin"
        )

        with RingBuffer(filename=filename, capacity=4) as buf:
            self.assertTrue(buf.write(10, "B", 150, 2))
            self.assertEqual(buf.read()["order_id"], 10)

        self.assertTrue(buf.memory.closed)
        self.assertTrue(buf.file.closed)


if __name__ == "__main__":
    unittest.main()
