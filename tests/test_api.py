from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_analyze_endpoint():
    response = client.post(
        "/analyze",
        json={"message": "Win lottery now pay fee"},
        headers={"x-api-key": "HCL123"}
    )
    assert response.status_code == 200
    assert "scam_detected" in response.json()
