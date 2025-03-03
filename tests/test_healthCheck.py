from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """ Test if the /health endpoint is working correctly. """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
