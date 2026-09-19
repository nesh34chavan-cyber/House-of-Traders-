from app.models.schemas import AnalysisResponse

def analyze_market(symbol: str) -> AnalysisResponse:
    # Deliberately conservative until validated live/historical data is supplied.
    return AnalysisResponse(
        symbol=symbol,
        regime="UNKNOWN",
        bias="NEUTRAL",
        confidence=0.0,
        factors=[
            "Validated market data is not connected",
            "No stale or synthetic price is used",
            "No trading conclusion is generated"
        ],
        invalidation="N/A",
        note="Connect a validated provider and feature pipeline before live analysis."
    )
