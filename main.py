
class ChronosMatch:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_buy_order(self, order_id, price, quantity):
        order = {
            "id": order_id,
            "price": price,
            "quantity": quantity
        }

        self.buy_orders.append(order)
        print("Buy order added:", order)

        # Try matching with existing sell orders
        self.match_orders()

    def add_sell_order(self, order_id, price, quantity):
        order = {
            "id": order_id,
            "price": price,
            "quantity": quantity
        }

        self.sell_orders.append(order)
        print("Sell order added:", order)

        # Try matching with existing buy orders
        self.match_orders()

    def match_orders(self):
        matches = []

        while self.buy_orders and self.sell_orders:
            buy = self.buy_orders[0]
            sell = self.sell_orders[0]

            # No match if the buy price is below the sell price
            if buy["price"] < sell["price"]:
                break

            # Execute the trade for the smaller quantity
            traded_quantity = min(
                buy["quantity"],
                sell["quantity"]
            )

            trade = {
                "buy_order_id": buy["id"],
                "sell_order_id": sell["id"],
                "price": sell["price"],
                "quantity": traded_quantity
            }

            matches.append(trade)
            print("Trade executed:", trade)

            # Update remaining quantities
            buy["quantity"] -= traded_quantity
            sell["quantity"] -= traded_quantity

            # Remove fully completed orders
            if buy["quantity"] == 0:
                self.buy_orders.pop(0)

            if sell["quantity"] == 0:
                self.sell_orders.pop(0)

        return matches


if __name__ == "__main__":
    engine = ChronosMatch()

    print("ChronosMatch Trading Engine Started")

    engine.add_buy_order(1, 105, 10)
    engine.add_sell_order(2, 100, 5)

    print("\n--- Remaining Buy Orders ---")
    print(engine.buy_orders)

    print("\n--- Remaining Sell Orders ---")
    print(engine.sell_orders)
