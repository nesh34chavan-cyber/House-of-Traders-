from fastapi import APIRouter, HTTPException
from .backtest import run_sma_cross
from .market import TIMEFRAMES, market_service
from .paper import paper_broker
from .research import research
from .risk import calculate_position_size
from .schemas import AnalysisResponse, BacktestRequest, BacktestResult, Candle, MarketSnapshot, MarketTick, PaperOrder, ResearchRequest, RiskRequest, RiskResponse

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/status")
def status():
    return {"api": "ok", "market_data": "ingestion-ready", "database": "not-connected",
            "redis": "not-connected", "execution": "paper-only"}

@router.get("/symbols")
def symbols():
    return {"symbols": ["XAUUSD", "XAGUSD", "EURUSD", "GBPUSD", "USDJPY", "DXY", "BTCUSD"]}

@router.get("/market/{symbol}", response_model=MarketSnapshot)
def market(symbol: str):
    return market_service.snapshot(symbol.upper())

@router.get("/candles/{symbol}/{timeframe}", response_model=list[Candle])
def candles(symbol: str, timeframe: str):
    try:
        return market_service.get_candles(symbol.upper(), timeframe)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/market/tick")
def tick(payload: MarketTick):
    completed = market_service.update_tick(payload)
    return {"accepted": True, "symbol": payload.symbol, "completed_candles": completed}

@router.get("/analysis/{symbol}", response_model=AnalysisResponse)
def analysis(symbol: str):
    snap = market_service.snapshot(symbol.upper())
    if snap["price"] is None:
        return AnalysisResponse(symbol=symbol.upper(), regime="UNKNOWN", bias="NEUTRAL",
                                confidence=0, factors=[], invalidation="Unavailable",
                                note="No validated market data connected.")
    return AnalysisResponse(symbol=symbol.upper(), regime="DATA-ONLY", bias="NEUTRAL",
                            confidence=0, factors=["Validated tick received"],
                            invalidation="Data quality failure",
                            note="Signal engines remain disabled until historical/live data validation is configured.")

@router.post("/risk/position-size", response_model=RiskResponse)
def risk(req: RiskRequest):
    return calculate_position_size(req)

@router.post("/backtest/sma-cross", response_model=BacktestResult)
def backtest(req: BacktestRequest):
    return run_sma_cross(req.candles, req.fast, req.slow, req.initial_equity, req.risk_fraction)

@router.post("/paper/order")
def paper_order(req: PaperOrder):
    return paper_broker.order(req.symbol.upper(), req.side, req.quantity, req.price)

@router.get("/paper/portfolio")
def portfolio():
    return paper_broker.snapshot()

@router.post("/research")
def do_research(req: ResearchRequest):
    return research(req.symbol.upper(), req.question, req.evidence)
