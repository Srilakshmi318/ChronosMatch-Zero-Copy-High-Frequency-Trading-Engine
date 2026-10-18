
import time

class ChronosMatch:
    def __init__(self):
        self.orders = []

    def add_order(self, order_id, price, quantity):
        order = {
            "id": order_id,
            "price": price,
            "quantity": quantity
        }
        self.orders.append(order)
        print(f"Order added: {order}")

    def show_orders(self):
        print("\n--- ChronosMatch Order Book ---")
        for order in self.orders:
            print(order)


if __name__ == "__main__":
    print("ChronosMatch Trading Engine Started")
    engine = ChronosMatch()

    engine.add_order(1, 100.50, 10)
    engine.add_order(2, 101.00, 5)
    engine.show_orders()
