class PaperBroker:
    def __init__(self, equity=10000.0): self.equity=equity; self.positions={}; self.orders=[]
    def order(self, symbol, side, quantity, price):
        signed=quantity if side=='BUY' else -quantity
        p=self.positions.get(symbol)
        if p and ((p['quantity']>0) != (signed>0)):
            newq=p['quantity']+signed
            if newq==0: self.positions.pop(symbol)
            else: p['quantity']=newq
        elif p:
            total=p['quantity']+signed; p['average_price']=(p['average_price']*p['quantity']+price*signed)/total; p['quantity']=total
        else:
            self.positions[symbol]={'symbol':symbol,'side':'LONG' if signed>0 else 'SHORT','quantity':signed,'average_price':price}
        self.orders.append({'symbol':symbol,'side':side,'quantity':quantity,'price':price})
        return self.orders[-1]
    def snapshot(self): return {'equity':self.equity,'positions':list(self.positions.values()),'orders':self.orders[-50:]}
paper_broker=PaperBroker()
