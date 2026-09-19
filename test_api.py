from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'

def test_symbols():
    r = client.get('/api/v1/symbols')
    assert r.status_code == 200
    assert 'XAUUSD' in r.json()['symbols']

def test_market_is_explicitly_unconfigured():
    r = client.get('/api/v1/market/XAUUSD')
    assert r.status_code == 200
    assert r.json()['status'] == 'provider-not-configured'

def test_analysis_is_conservative_without_data():
    r = client.get('/api/v1/analysis/XAUUSD')
    assert r.status_code == 200
    assert r.json()['bias'] == 'NEUTRAL'
    assert r.json()['confidence'] == 0

def test_risk_position_size():
    r = client.post('/api/v1/risk/position-size', json={'equity':10000,'risk_fraction':0.01,'entry':3000,'stop':2990,'point_value':1})
    assert r.status_code == 200
    assert r.json()['risk_amount'] == 100
    assert r.json()['stop_distance'] == 10
    assert r.json()['units'] == 10
