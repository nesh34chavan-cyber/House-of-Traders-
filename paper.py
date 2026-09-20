class PaperBroker:
    def __init__(self, equity=10000.0):
        self.equity = equity
        self.positions = {}
        self.orders = []

    def order(self, symbol, side, quantity, price):
        signed = quantity if side == "BUY" else -quantity
        position = self.positions.get(symbol)
        if position and ((position["quantity"] > 0) != (signed > 0)):
            new_quantity = position["quantity"] + signed
            if new_quantity == 0:
                self.positions.pop(symbol)
            else:
                position["quantity"] = new_quantity
        elif position:
            total = position["quantity"] + signed
            position["average_price"] = (
                position["average_price"]*position["quantity"] + price*signed
            ) / total
            position["quantity"] = total
        else:
            self.positions[symbol] = {
                "symbol": symbol, "side": "LONG" if signed > 0 else "SHORT",
                "quantity": signed, "average_price": price
            }
        order = {"symbol": symbol, "side": side, "quantity": quantity, "price": price}
        self.orders.append(order)
        return order

    def snapshot(self):
        return {"equity": self.equity, "positions": list(self.positions.values()),
                "orders": self.orders[-50:]}

paper_broker = PaperBroker()
