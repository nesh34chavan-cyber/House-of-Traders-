from fastapi import APIRouter, HTTPException
from ..models.schemas import *
from ..services.market import market_service
from ..services.backtest import run_sma_cross
from ..services.paper import paper_broker
from ..services.research import research
router=APIRouter()

@router.get('/health')
def health(): return {'status':'ok'}
@router.get('/status')
def status(): return {'api':'ok','market_data':'adapter-ready','database':'configured-by-env','redis':'configured-by-env','execution':'paper-only'}
@router.get('/symbols')
def symbols(): return {'symbols':['XAUUSD','XAGUSD','EURUSD','GBPUSD','USDJPY','DXY','BTCUSD']}
@router.get('/market/{symbol}',response_model=MarketSnapshot)
def market(symbol:str): return market_service.snapshot(symbol.upper())
@router.get('/candles/{symbol}/{timeframe}',response_model=list[Candle])
def candles(symbol:str,timeframe:str): return market_service.get_candles(symbol.upper(),timeframe)
@router.post('/market/tick')
def tick(payload:dict):
    required={'symbol','price'}
    if not required.issubset(payload): raise HTTPException(400,'symbol and price are required')
    return {'completed_candles':market_service.update_tick(payload['symbol'].upper(),float(payload['price']),payload.get('bid'),payload.get('ask'),float(payload.get('volume',0)))}
@router.get('/analysis/{symbol}',response_model=AnalysisResponse)
def analysis(symbol:str):
    snap=market_service.snapshot(symbol.upper())
    if snap['price'] is None: return AnalysisResponse(symbol=symbol.upper(),regime='UNKNOWN',bias='NEUTRAL',confidence=0,factors=[],invalidation='Unavailable',note='No validated market data connected.')
    return AnalysisResponse(symbol=symbol.upper(),regime='DATA-ONLY',bias='NEUTRAL',confidence=0,factors=['Live tick received'],invalidation='Data quality failure',note='Signal engines activate only after validated historical/live data is configured.')
@router.post('/risk/position-size',response_model=RiskResponse)
def risk(req:RiskRequest):
    amount=req.equity*req.risk_fraction; dist=abs(req.entry-req.stop); units=amount/(dist*req.point_value) if dist else 0
    return RiskResponse(risk_amount=amount,stop_distance=dist,units=units,risk_fraction=req.risk_fraction)
@router.post('/backtest/sma-cross',response_model=BacktestResult)
def backtest(req:BacktestRequest): return run_sma_cross(req.candles,req.fast,req.slow,req.initial_equity,req.risk_fraction)
@router.post('/paper/order')
def paper_order(req:PaperOrder): return paper_broker.order(req.symbol,req.side,req.quantity,req.price)
@router.get('/paper/portfolio')
def portfolio(): return paper_broker.snapshot()
@router.post('/research')
def do_research(req:ResearchRequest): return research(req.symbol,req.question,req.evidence)
