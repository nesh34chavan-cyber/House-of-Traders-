from datetime import datetime, timezone
from .candles import CandleBuilder
from .schemas import MarketTick

TIMEFRAMES = ("1m", "5m", "15m", "30m", "1h", "4h", "1d")

class MarketService:
    def __init__(self):
        self.snapshots = {}
        self.candles = {}
        self.builders = {}

    def update_tick(self, tick: MarketTick):
        ts = tick.timestamp or datetime.now(timezone.utc)
        self.snapshots[tick.symbol] = {
            "symbol": tick.symbol, "timestamp": ts, "price": tick.price,
            "bid": tick.bid, "ask": tick.ask, "status": "live",
            "provider": "ingestion",
        }
        completed = []
        for tf in TIMEFRAMES:
            key = (tick.symbol, tf)
            builder = self.builders.setdefault(key, CandleBuilder(tick.symbol, tf))
            candle = builder.update(ts, tick.price, tick.volume)
            if candle:
                self.candles.setdefault(key, []).append(candle)
                self.candles[key] = self.candles[key][-5000:]
                completed.append(candle)
        return completed

    def snapshot(self, symbol: str):
        return self.snapshots.get(symbol, {
            "symbol": symbol,
            "timestamp": datetime.now(timezone.utc),
            "price": None, "bid": None, "ask": None,
            "status": "provider-not-configured", "provider": "none",
        })

    def get_candles(self, symbol: str, timeframe: str, limit: int = 500):
        if timeframe not in TIMEFRAMES:
            raise ValueError(f"Unsupported timeframe: {timeframe}")
        return self.candles.get((symbol, timeframe), [])[-min(limit, 5000):]

market_service = MarketService()
