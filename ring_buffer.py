
import mmap
import math
import os
import struct
import time

BUFFER_FILE = "orders_buffer.bin"
CAPACITY = 1024

HEADER = struct.Struct("<II")
ORDER = struct.Struct("<IBqIQ")

HEADER_SIZE = HEADER.size
BUFFER_SIZE = HEADER_SIZE + CAPACITY * ORDER.size


class RingBuffer:
    def __init__(self, filename=BUFFER_FILE, capacity=CAPACITY):
        if type(capacity) is not int or capacity < 2:
            raise ValueError("Capacity must be an integer of at least 2")

        self.filename = filename
        self.capacity = capacity
        self.header = HEADER
        self.order = ORDER
        self.header_size = HEADER.size
        self.buffer_size = HEADER.size + capacity * ORDER.size

        self.file = open(filename, "w+b")
        self.file.truncate(self.buffer_size)

        try:
            self.memory = mmap.mmap(
                self.file.fileno(), self.buffer_size
            )
            self.header.pack_into(self.memory, 0, 0, 0)
        except Exception:
            self.file.close()
            raise

    def write(self, order_id, side, price, quantity):
        if type(order_id) is not int or not 0 <= order_id <= 0xFFFFFFFF:
            raise ValueError("Invalid order ID")

        if not isinstance(side, str) or side.upper() not in ("B", "S"):
            raise ValueError("Side must be B or S")

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise ValueError("Price must be numeric")

        if not math.isfinite(price) or price <= 0:
            raise ValueError("Price must be positive and finite")

        if type(quantity) is not int or not 0 < quantity <= 0xFFFFFFFF:
            raise ValueError("Quantity must be a positive 32-bit integer")

        price_paise = round(price * 100)

        if not 0 < price_paise <= 0x7FFFFFFFFFFFFFFF:
            raise ValueError("Price is outside supported range")

        write_pos, read_pos = self.header.unpack_from(
            self.memory, 0
        )

        next_pos = (write_pos + 1) % self.capacity

        if next_pos == read_pos:
            return False

        side_code = 1 if side.upper() == "B" else 2
        timestamp_ns = time.perf_counter_ns()

        offset = self.header_size + write_pos * self.order.size

        self.order.pack_into(
            self.memory,
            offset,
            order_id,
            side_code,
            price_paise,
            quantity,
            timestamp_ns,
        )

        self.header.pack_into(
            self.memory, 0, next_pos, read_pos
        )

        return True

    def read(self):
        write_pos, read_pos = self.header.unpack_from(
            self.memory, 0
        )

        if read_pos == write_pos:
            return None

        offset = self.header_size + read_pos * self.order.size

        order_id, side, price, quantity, timestamp = (
            self.order.unpack_from(self.memory, offset)
        )

        next_read = (read_pos + 1) % self.capacity

        self.header.pack_into(
            self.memory, 0, write_pos, next_read
        )

        return {
            "order_id": order_id,
            "side": "BUY" if side == 1 else "SELL",
            "price": price / 100,
            "quantity": quantity,
            "timestamp_ns": timestamp,
        }

    def close(self):
        if not self.memory.closed:
            self.memory.close()

        if not self.file.closed:
            self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass


if __name__ == "__main__":
    with RingBuffer() as buffer:
        buffer.write(1, "B", 150.25, 10)
        buffer.write(2, "S", 150.25, 5)

        print("Order 1:", buffer.read())
        print("Order 2:", buffer.read())
        print("Empty buffer:", buffer.read())
