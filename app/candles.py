from dataclasses import dataclass
from datetime import datetime, timezone


TIMEFRAME_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "30m": 1800,
    "1h": 3600,
    "4h": 14400,
    "1d": 86400,
}


def bucket_time(ts: datetime, seconds: int) -> datetime:
    ts = ts.astimezone(timezone.utc)
    epoch = int(ts.timestamp())
    return datetime.fromtimestamp(
        epoch - epoch % seconds,
        tz=timezone.utc,
    )


@dataclass
class CandleBuilder:
    symbol: str
    timeframe: str
    _current: dict | None = None

    def __post_init__(self):
        if self.timeframe not in TIMEFRAME_SECONDS:
            raise ValueError(
                f"Unsupported timeframe: {self.timeframe}"
            )

    def update(
        self,
        timestamp: datetime,
        price: float,
        volume: float = 0.0,
    ):
        if price <= 0:
            raise ValueError("price must be positive")

        bucket = bucket_time(
            timestamp,
            TIMEFRAME_SECONDS[self.timeframe],
        )

        if (
            self._current is None
            or bucket > self._current["timestamp"]
        ):
            completed = self._current

            self._current = {
                "symbol": self.symbol,
                "timeframe": self.timeframe,
                "timestamp": bucket,
                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "volume": volume,
            }

            return completed

        if bucket < self._current["timestamp"]:
            return None

        candle = self._current

        candle["high"] = max(
            candle["high"],
            price,
        )

        candle["low"] = min(
            candle["low"],
            price,
        )

        candle["close"] = price
        candle["volume"] += volume

        return None

    def flush(self):
        candle = self._current
        self._current = None
        return candle
