from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

Bias = Literal['BULLISH','BEARISH','NEUTRAL']

class MarketSnapshot(BaseModel):
    symbol: str
    timestamp: datetime
    price: float | None = None
    bid: float | None = None
    ask: float | None = None
    status: str
    provider: str

class Candle(BaseModel):
    symbol: str
    timeframe: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

class AnalysisResponse(BaseModel):
    symbol: str
    regime: str
    bias: Bias
    confidence: float = Field(ge=0, le=1)
    factors: list[str]
    invalidation: str
    note: str

class RiskRequest(BaseModel):
    equity: float = Field(gt=0)
    risk_fraction: float = Field(gt=0, le=0.1)
    entry: float = Field(gt=0)
    stop: float = Field(gt=0)
    point_value: float = Field(gt=0)

class RiskResponse(BaseModel):
    risk_amount: float
    stop_distance: float
    units: float
    risk_fraction: float

class BacktestRequest(BaseModel):
    candles: list[Candle]
    fast: int = Field(default=20, ge=2, le=500)
    slow: int = Field(default=50, ge=3, le=1000)
    initial_equity: float = Field(default=10000, gt=0)
    risk_fraction: float = Field(default=0.005, gt=0, le=0.1)

class BacktestTrade(BaseModel):
    entry_time: datetime
    exit_time: datetime
    side: Literal['LONG','SHORT']
    entry: float
    exit: float
    pnl: float

class BacktestResult(BaseModel):
    trades: list[BacktestTrade]
    initial_equity: float
    final_equity: float
    return_pct: float
    max_drawdown_pct: float
    win_rate: float
    profit_factor: float

class PaperOrder(BaseModel):
    symbol: str
    side: Literal['BUY','SELL']
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)

class PaperPosition(BaseModel):
    symbol: str
    side: Literal['LONG','SHORT']
    quantity: float
    average_price: float

class ResearchRequest(BaseModel):
    symbol: str
    question: str
    evidence: list[str] = []
