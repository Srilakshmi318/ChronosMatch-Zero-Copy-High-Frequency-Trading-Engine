
import time
from main import ChronosMatch

engine = ChronosMatch()

number_of_orders = 10000

start_time = time.perf_counter()

for order_id in range(number_of_orders):
    engine.add_buy_order(order_id, 100.0, 1)

elapsed_time = time.perf_counter() - start_time

orders_per_second = number_of_orders / elapsed_time

print("\n--- Benchmark Results ---")
print(f"Orders added: {number_of_orders}")
print(f"Elapsed time: {elapsed_time:.6f} seconds")
print(f"Order submissions per second: {orders_per_second:.2f}")
