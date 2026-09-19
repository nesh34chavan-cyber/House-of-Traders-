from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.services.candles import CandleBuilder
c=TestClient(app)

def test_health(): assert c.get('/api/v1/health').json()['status']=='ok'
def test_tick_and_candle_builder():
    b=CandleBuilder('XAUUSD','1m'); t=datetime(2026,1,1,tzinfo=timezone.utc)
    assert b.update(t,2000) is None
    out=b.update(t+timedelta(seconds=60),2001)
    assert out['open']==2000 and out['close']==2000

def test_risk():
    r=c.post('/api/v1/risk/position-size',json={'equity':10000,'risk_fraction':0.01,'entry':2000,'stop':1990,'point_value':1}).json()
    assert r['risk_amount']==100 and r['units']==10

def test_backtest():
    t=datetime(2026,1,1,tzinfo=timezone.utc)
    candles=[]; prices=list(range(100,130))+list(range(130,100,-1))
    for i,p in enumerate(prices): candles.append({'symbol':'XAUUSD','timeframe':'1h','timestamp':(t+timedelta(hours=i)).isoformat(),'open':p,'high':p+1,'low':p-1,'close':p,'volume':1})
    r=c.post('/api/v1/backtest/sma-cross',json={'candles':candles,'fast':3,'slow':8}).json()
    assert 'final_equity' in r and len(r['trades'])>=1

def test_paper_order():
    r=c.post('/api/v1/paper/order',json={'symbol':'XAUUSD','side':'BUY','quantity':1,'price':2000}).json()
    assert r['symbol']=='XAUUSD'
