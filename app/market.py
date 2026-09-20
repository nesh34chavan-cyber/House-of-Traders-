from datetime import datetime, timezone

from .candles import CandleBuilder


TIMEFRAMES = (
    "1m",
    "5m",
    "15m",
    "30m",
    "1h",
    "4h",
    "1d",
)


class MarketService:
    def __init__(self):
        self.snapshots = {}
        self.candles = {}
        self.builders = {}
        self.subscribers = set()

    def update_tick(
        self,
        symbol,
        price,
        bid=None,
        ask=None,
        volume=0.0,
        timestamp=None,
    ):
        ts = timestamp or datetime.now(timezone.utc)

        self.snapshots[symbol] = {
            "symbol": symbol,
            "timestamp": ts,
            "price": price,
            "bid": bid,
            "ask": ask,
            "status": "live",
            "provider": "external",
        }

        completed = []

        for timeframe in TIMEFRAMES:
            key = (symbol, timeframe)

            builder = self.builders.setdefault(
                key,
                CandleBuilder(symbol, timeframe),
            )

            candle = builder.update(
                ts,
                price,
                volume,
            )

            if candle:
                self.candles.setdefault(
                    key,
                    [],
                ).append(candle)

                completed.append(candle)

        return completed

    def snapshot(self, symbol):
        return self.snapshots.get(
            symbol,
            {
                "symbol": symbol,
                "timestamp": datetime.now(timezone.utc),
                "price": None,
                "bid": None,
                "ask": None,
                "status": "provider-not-configured",
                "provider": "none",
            },
        )

    def get_candles(
        self,
        symbol,
        timeframe,
        limit=500,
    ):
        return self.candles.get(
            (symbol, timeframe),
            [],
        )[-limit:]


market_service = MarketService()
