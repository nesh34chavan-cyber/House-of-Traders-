class PaperBroker:
    def __init__(self):
        self.positions = {}
        self.orders = []

    def order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
    ):
        if quantity <= 0:
            raise ValueError("quantity must be positive")

        if price <= 0:
            raise ValueError("price must be positive")

        side = side.upper()

        if side not in {"BUY", "SELL"}:
            raise ValueError(
                "side must be BUY or SELL"
            )

        position_side = (
            "LONG"
            if side == "BUY"
            else "SHORT"
        )

        existing = self.positions.get(symbol)

        if existing is None:
            self.positions[symbol] = {
                "symbol": symbol,
                "side": position_side,
                "quantity": quantity,
                "average_price": price,
            }

        elif existing["side"] == position_side:
            old_quantity = existing["quantity"]
            new_quantity = old_quantity + quantity

            existing["average_price"] = (
                (
                    existing["average_price"]
                    * old_quantity
                )
                + (price * quantity)
            ) / new_quantity

            existing["quantity"] = new_quantity

        else:
            remaining = existing["quantity"] - quantity

            if remaining > 0:
                existing["quantity"] = remaining

            elif remaining == 0:
                del self.positions[symbol]

            else:
                self.positions[symbol] = {
                    "symbol": symbol,
                    "side": position_side,
                    "quantity": abs(remaining),
                    "average_price": price,
                }

        order = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
        }

        self.orders.append(order)

        return {
            "status": "filled",
            "order": order,
            "portfolio": self.snapshot(),
        }

    def snapshot(self):
        return {
            "positions": list(
                self.positions.values()
            ),
            "orders": self.orders,
        }


paper_broker = PaperBroker()
