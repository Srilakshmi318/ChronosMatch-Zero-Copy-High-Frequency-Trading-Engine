
import time
import math


class ChronosMatch:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.trade_history = []

    def validate_order(self, order_id, price, quantity):
        if not isinstance(order_id, int) or order_id < 0:
            raise ValueError("Invalid order ID")

        if not isinstance(price, (int, float)):
            raise ValueError("Price must be numeric")

        if not math.isfinite(price) or price <= 0:
            raise ValueError("Price must be positive and finite")

        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

    def add_buy_order(self, order_id, price, quantity):
        return self._add_order(
            order_id, price, quantity, "BUY"
        )

    def add_sell_order(self, order_id, price, quantity):
        return self._add_order(
            order_id, price, quantity, "SELL"
        )

    def _add_order(self, order_id, price, quantity, side):
        self.validate_order(order_id, price, quantity)

        order = {
            "id": order_id,
            "price": float(price),
            "quantity": quantity,
            "side": side,
            "timestamp": time.perf_counter_ns()
        }

        if side == "BUY":
            self.buy_orders.append(order)
            self.buy_orders.sort(
                key=lambda x: (-x["price"], x["timestamp"])
            )
        else:
            self.sell_orders.append(order)
            self.sell_orders.sort(
                key=lambda x: (x["price"], x["timestamp"])
            )

        return self.match_orders()

    def match_orders(self):
        new_trades = []

        while self.buy_orders and self.sell_orders:
            buy = self.buy_orders[0]
            sell = self.sell_orders[0]

            if buy["price"] < sell["price"]:
                break

            quantity = min(
                buy["quantity"],
                sell["quantity"]
            )

            # Execute at the older resting order's price.
            if buy["timestamp"] < sell["timestamp"]:
                execution_price = buy["price"]
            else:
                execution_price = sell["price"]

            trade = {
                "buy_order_id": buy["id"],
                "sell_order_id": sell["id"],
                "price": execution_price,
                "quantity": quantity,
                "timestamp": time.perf_counter_ns()
            }

            new_trades.append(trade)
            self.trade_history.append(trade)

            buy["quantity"] -= quantity
            sell["quantity"] -= quantity

            if buy["quantity"] == 0:
                self.buy_orders.pop(0)

            if sell["quantity"] == 0:
                self.sell_orders.pop(0)

        return new_trades

    def display_order_book(self):
        print("\n--- BUY ORDERS ---")
        for order in self.buy_orders:
            print(order)

        print("\n--- SELL ORDERS ---")
        for order in self.sell_orders:
            print(order)

    def display_trades(self):
        print("\n--- TRADE HISTORY ---")
        for trade in self.trade_history:
            print(trade)


if __name__ == "__main__":
    engine = ChronosMatch()

    print("ChronosMatch Engine Started")

    engine.add_buy_order(1, 105, 10)
    engine.add_sell_order(2, 100, 5)
    engine.add_sell_order(3, 105, 3)

    engine.display_order_book()
    engine.display_trades()
