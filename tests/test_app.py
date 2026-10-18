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


def test_safe_log_redacts_credentials():
    from app import safe_log

    log = (
        "Authorization: Bearer demoBearer123\n"
        "api_key=demoApiKey123\n"
        "password: demoPassword123\n"
        "AKIA1234567890ABCDEF\n"
        "ghp_" + "A" * 25 + "\n"
        "gsk_" + "B" * 25 + "\n"
        "Build completed successfully"
    )

    result = safe_log(log)

    for secret in (
        "demoBearer123",
        "demoApiKey123",
        "demoPassword123",
        "AKIA1234567890ABCDEF",
        "ghp_" + "A" * 25,
        "gsk_" + "B" * 25,
    ):
        assert secret not in result

    assert "Build completed successfully" in result
