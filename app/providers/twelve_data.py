from datetime import datetime, timezone
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from ..config import settings


SYMBOL_MAP = {
    "XAUUSD": "XAU/USD",
    "XAGUSD": "XAG/USD",
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY",
    "BTCUSD": "BTC/USD",
}


class TwelveDataError(RuntimeError):
    pass


def normalize_symbol(symbol: str) -> str:
    key = symbol.strip().upper()
    return SYMBOL_MAP.get(key, key)


def fetch_price(symbol: str) -> dict:
    if not settings.twelve_data_api_key:
        raise TwelveDataError(
            "TWELVE_DATA_API_KEY is not configured"
        )

    provider_symbol = normalize_symbol(symbol)

    params = urlencode({
        "symbol": provider_symbol,
        "apikey": settings.twelve_data_api_key,
        "dp": 8,
    })

    url = (
        f"{settings.twelve_data_base_url.rstrip('/')}"
        f"/price?{params}"
    )

    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Traders-Inc-Terminal/0.2",
        },
    )

    try:
        with urlopen(request, timeout=10) as response:
            payload = json.loads(
                response.read().decode("utf-8")
            )

    except HTTPError as exc:
        raise TwelveDataError(
            f"Twelve Data HTTP {exc.code}"
        ) from exc

    except (URLError, TimeoutError) as exc:
        raise TwelveDataError(
            "Unable to reach Twelve Data"
        ) from exc

    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise TwelveDataError(
            "Invalid response from Twelve Data"
        ) from exc

    if (
        payload.get("status") == "error"
        or (
            "code" in payload
            and "price" not in payload
        )
    ):
        message = payload.get(
            "message",
            "Twelve Data request failed"
        )

        raise TwelveDataError(message)

    try:
        price = float(payload["price"])

    except (KeyError, TypeError, ValueError) as exc:
        raise TwelveDataError(
            "Twelve Data returned no valid price"
        ) from exc

    if price <= 0:
        raise TwelveDataError(
            "Twelve Data returned an invalid price"
        )

    return {
        "symbol": symbol.upper(),
        "provider_symbol": provider_symbol,
        "price": price,
        "timestamp": datetime.now(timezone.utc),
        "provider": "twelve_data",
    }
