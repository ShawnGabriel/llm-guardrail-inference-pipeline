from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_generate_basic():
    payload = {
        "prompt": "Explain what a transformer model is in 2 sentences.",
        "max_new_tokens": 32,
        "enable_agent": False,
        "temperature": 0.7
    }
    resp = client.post("/generate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "flags" in data
