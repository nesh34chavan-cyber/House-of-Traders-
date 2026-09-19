from abc import ABC, abstractmethod
from typing import Optional
from app.models.schemas import MarketSnapshot

class MarketDataProvider(ABC):
    name: str = "unknown"

    @abstractmethod
    def snapshot(self, symbol: str) -> MarketSnapshot:
        raise NotImplementedError

class NoMarketDataProvider(MarketDataProvider):
    name = "none"

    def snapshot(self, symbol: str) -> MarketSnapshot:
        from datetime import datetime, timezone
        return MarketSnapshot(
            symbol=symbol.upper(), timestamp=datetime.now(timezone.utc),
            status="provider-not-configured", provider=self.name
        )
