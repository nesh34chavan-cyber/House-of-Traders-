# Trader's Inc Terminal — V1 Engineering Build

A modular trading research and terminal foundation. This repository is designed for real providers and paper/live separation; it does not fabricate market prices or AI signals.

## Included
- FastAPI backend
- Market tick ingestion endpoint
- Multi-timeframe candle builder (1m/5m/15m/30m/1h/4h/1d)
- Market snapshot API
- Conservative analysis API
- Risk sizing API
- SMA-cross backtest API with drawdown/profit-factor metrics
- Paper broker and portfolio API
- Evidence-grounded research endpoint
- Terminal frontend
- Automated tests

## Run
```bash
cd backend
python -m pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload --port 8000
```
Open `frontend/index.html` or serve the frontend with a local static server.

## Feed a test tick
```bash
curl -X POST http://localhost:8000/api/v1/market/tick -H 'content-type: application/json' -d '{"symbol":"XAUUSD","price":3650.25,"bid":3650.10,"ask":3650.40,"volume":1}'
```

## Architecture
Provider adapters should call `/market/tick` or a dedicated ingestion service. Production deployment should persist candles to TimescaleDB, stream via Redis/WebSockets, and keep paper/live execution isolated. Broker credentials must never be committed.
