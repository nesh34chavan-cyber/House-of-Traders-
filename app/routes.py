from fastapi import APIRouter, HTTPException

from .backtest import run_sma_cross
from .market import market_service
from .paper import paper_broker
from .research import research
from .risk import calculate_position_size
from .schemas import (
    AnalysisResponse,
    BacktestRequest,
    BacktestResult,
    Candle,
    MarketSnapshot,
    MarketTick,
    PaperOrder,
    ResearchRequest,
    RiskRequest,
    RiskResponse,
)


router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "traders-inc-terminal-api",
    }


@router.get("/status")
def status():
    return {
        "api": "ok",
        "market_data": "adapter-ready",
        "database": "configured-by-env",
        "redis": "configured-by-env",
        "execution": "paper-only",
    }


@router.get("/symbols")
def symbols():
    return {
        "symbols": [
            "XAUUSD",
            "XAGUSD",
            "EURUSD",
            "GBPUSD",
            "USDJPY",
            "DXY",
            "BTCUSD",
        ]
    }


@router.get(
    "/market/{symbol}",
    response_model=MarketSnapshot,
)
def market(symbol: str):
    return market_service.snapshot(
        symbol.upper()
    )


@router.get(
    "/candles/{symbol}/{timeframe}",
    response_model=list[Candle],
)
def candles(
    symbol: str,
    timeframe: str,
):
    return market_service.get_candles(
        symbol.upper(),
        timeframe,
    )


@router.post("/market/tick")
def tick(payload: MarketTick):
    completed = market_service.update_tick(
        symbol=payload.symbol,
        price=payload.price,
        bid=payload.bid,
        ask=payload.ask,
        volume=payload.volume,
        timestamp=payload.timestamp,
    )

    return {
        "accepted": True,
        "symbol": payload.symbol,
        "price": payload.price,
        "completed_candles": completed,
    }


@router.get(
    "/analysis/{symbol}",
    response_model=AnalysisResponse,
)
def analysis(symbol: str):
    snapshot = market_service.snapshot(
        symbol.upper()
    )

    if snapshot["price"] is None:
        return AnalysisResponse(
            symbol=symbol.upper(),
            regime="UNKNOWN",
            bias="NEUTRAL",
            confidence=0,
            factors=[
                "Validated market data is not connected",
                "No synthetic price is used",
            ],
            invalidation="Unavailable",
            note=(
                "Connect a validated market "
                "data provider before analysis."
            ),
        )

    return AnalysisResponse(
        symbol=symbol.upper(),
        regime="DATA-ONLY",
        bias="NEUTRAL",
        confidence=0,
        factors=[
            "Validated tick received",
            "Signal engine not activated",
        ],
        invalidation="Data quality failure",
        note=(
            "Signal engines activate only after "
            "validated historical/live data is configured."
        ),
    )


@router.post(
    "/risk/position-size",
    response_model=RiskResponse,
)
def risk(req: RiskRequest):
    try:
        result = calculate_position_size(
            equity=req.equity,
            risk_fraction=req.risk_fraction,
            entry=req.entry,
            stop=req.stop,
            point_value=req.point_value,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return RiskResponse(**result)


@router.post(
    "/backtest/sma-cross",
    response_model=BacktestResult,
)
def backtest(req: BacktestRequest):
    try:
        return run_sma_cross(
            candles=req.candles,
            fast=req.fast,
            slow=req.slow,
            initial_equity=req.initial_equity,
            risk_fraction=req.risk_fraction,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post("/paper/order")
def paper_order(req: PaperOrder):
    try:
        return paper_broker.order(
            symbol=req.symbol.upper(),
            side=req.side,
            quantity=req.quantity,
            price=req.price,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get("/paper/portfolio")
def portfolio():
    return paper_broker.snapshot()


@router.post("/research")
def do_research(req: ResearchRequest):
    try:
        return research(
            symbol=req.symbol,
            question=req.question,
            evidence=req.evidence,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
