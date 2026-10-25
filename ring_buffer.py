
import mmap
import os
import struct
import time

# Buffer configuration
BUFFER_FILE = "orders_buffer.bin"
CAPACITY = 1024

# Header: write position and read position
HEADER = struct.Struct("<II")

# Order: ID, side, price in paise, quantity, timestamp
ORDER = struct.Struct("<IBqIQ")

HEADER_SIZE = HEADER.size
BUFFER_SIZE = HEADER_SIZE + CAPACITY * ORDER.size


class RingBuffer:
    def __init__(self, filename=BUFFER_FILE, capacity=CAPACITY):
        self.filename = filename
        self.capacity = capacity
        self.header = HEADER
        self.order = ORDER
        self.header_size = HEADER.size
        self.buffer_size = (
            self.header_size + capacity * ORDER.size
        )

        # Create or reset the backing file for this run.
        with open(filename, "wb") as file:
            file.truncate(self.buffer_size)

        self.file = open(filename, "r+b")
        self.memory = mmap.mmap(
            self.file.fileno(), self.buffer_size
        )

        self.header.pack_into(self.memory, 0, 0, 0)

    def write(self, order_id, side, price, quantity):
        write_pos, read_pos = self.header.unpack_from(
            self.memory, 0
        )

        next_pos = (write_pos + 1) % self.capacity

        if next_pos == read_pos:
            return False  # Buffer is full

        side_code = 1 if side.upper() == "B" else 2

        # Store price as integer paise to avoid float errors.
        price_paise = round(price * 100)
        timestamp_ns = time.perf_counter_ns()

        offset = (
            self.header_size + write_pos * self.order.size
        )

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
            return None  # Buffer is empty

        offset = (
            self.header_size + read_pos * self.order.size
        )

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
        self.memory.close()
        self.file.close()


if __name__ == "__main__":
    buffer = RingBuffer()

    try:
        buffer.write(1, "B", 150.25, 10)
        buffer.write(2, "S", 150.25, 5)

        print("Order 1:", buffer.read())
        print("Order 2:", buffer.read())
        print("Empty buffer:", buffer.read())
    finally:
        buffer.close()
