
import os
import tempfile
import time

from ring_buffer import RingBuffer

NUMBER_OF_ORDERS = 10000
CAPACITY = 1024


def run_benchmark():
    write_time = 0.0
    read_time = 0.0
    processed = 0

    with tempfile.TemporaryDirectory() as temp_dir:
        filename = os.path.join(temp_dir, "benchmark.bin")

        with RingBuffer(filename, CAPACITY) as buffer:
            while processed < NUMBER_OF_ORDERS:
                batch_size = min(
                    CAPACITY - 1,
                    NUMBER_OF_ORDERS - processed
                )

                # Measure writing
                start = time.perf_counter()

                for order_id in range(
                    processed, processed + batch_size
                ):
                    success = buffer.write(
                        order_id, "B", 100.0, 1
                    )

                    if not success:
                        raise RuntimeError("Buffer unexpectedly full")

                write_time += time.perf_counter() - start

                # Measure reading
                start = time.perf_counter()

                for expected_id in range(
                    processed, processed + batch_size
                ):
                    order = buffer.read()

                    if order is None:
                        raise RuntimeError("Buffer unexpectedly empty")

                    if order["order_id"] != expected_id:
                        raise RuntimeError("FIFO order verification failed")

                read_time += time.perf_counter() - start

                processed += batch_size

    print("\n--- Ring Buffer Benchmark Results ---")
    print(f"Orders processed: {processed}")
    print(f"Write time: {write_time:.6f} seconds")
    print(f"Read time: {read_time:.6f} seconds")
    print(f"Write throughput: {processed / write_time:.2f} orders/second")
    print(f"Read throughput: {processed / read_time:.2f} orders/second")
    print(
        f"Combined time: {write_time + read_time:.6f} seconds"
    )
    print(
        f"Combined throughput: "
        f"{processed / (write_time + read_time):.2f} orders/second"
    )


if __name__ == "__main__":
    run_benchmark()
