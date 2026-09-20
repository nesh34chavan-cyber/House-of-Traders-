# House of Traders — V0.2 Backend

FastAPI backend foundation for validated market-data ingestion, multi-timeframe candle building, analysis contracts, risk, backtesting and paper execution.

## Run
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

## Endpoints
GET /health
GET /api/v1/status
GET /api/v1/symbols
GET /api/v1/market/XAUUSD
GET /api/v1/candles/XAUUSD/1m
POST /api/v1/market/tick

## Test tick
POST /api/v1/market/tick
{"symbol":"XAUUSD","price":3650.25,"bid":3650.10,"ask":3650.40,"volume":1}

No real provider is hard-coded. Provider credentials belong in environment variables, never in Git.
