import pytest
from fastapi.testclient import TestClient
from app.main import app  # adjust path to your FastAPI app

client = TestClient(app)


def test_healthcheck():
    """Check if backend is alive"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_redirect():
    """Root should redirect or return a simple message"""
    response = client.get("/")
    assert response.status_code in (200, 307, 308)
