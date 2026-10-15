from app import app

def test_health():
    r = app.test_client().get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_empty_log_rejected():
    assert app.test_client().post("/api/analyze-log", json={"log": ""}).status_code == 400

def test_migration_risk():
    data = app.test_client().post("/api/risk-score", json={"paths": ["db/migrations/001.sql"]}).get_json()
    assert data["score"] >= 5
