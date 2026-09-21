from datetime import datetime, timezone, timedelta

from fastapi.testclient import TestClient

from app.main import app
from app.candles import CandleBuilder


client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_tick_and_candle_builder():
    builder = CandleBuilder("XAUUSD", "1m")

    timestamp = datetime(
        2026,
        1,
        1,
        tzinfo=timezone.utc,
    )

    assert builder.update(timestamp, 2000) is None

    completed = builder.update(
        timestamp + timedelta(seconds=60),
        2001,
    )

    assert completed["open"] == 2000
    assert completed["close"] == 2000


def test_risk():
    response = client.post(
        "/api/v1/risk/position-size",
        json={
            "equity": 10000,
            "risk_fraction": 0.01,
            "entry": 2000,
            "stop": 1990,
            "point_value": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["risk_amount"] == 100
    assert data["units"] == 10


def test_backtest():
    timestamp = datetime(
        2026,
        1,
        1,
        tzinfo=timezone.utc,
    )

    candles = []

    prices = (
        list(range(100, 130))
        + list(range(130, 100, -1))
    )

    for i, price in enumerate(prices):
        candles.append(
            {
                "symbol": "XAUUSD",
                "timeframe": "1h",
                "timestamp": (
                    timestamp
                    + timedelta(hours=i)
                ).isoformat(),
                "open": price,
                "high": price + 1,
                "low": price - 1,
                "close": price,
                "volume": 1,
            }
        )

    response = client.post(
        "/api/v1/backtest/sma-cross",
        json={
            "candles": candles,
            "fast": 3,
            "slow": 8,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "final_equity" in data
    assert len(data["trades"]) >= 1


def test_paper_order():
    response = client.post(
        "/api/v1/paper/order",
        json={
            "symbol": "XAUUSD",
            "side": "BUY",
            "quantity": 1,
            "price": 2000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "filled"
    assert data["order"]["symbol"] == "XAUUSD"
    assert data["order"]["side"] == "BUY"
