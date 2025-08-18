from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_users():
    """Mock DB call for /api/users"""
    fake_users = [{"id": 1, "name": "John"}]

    with patch("app.dependencies.get_users", return_value=fake_users):
        response = client.get("/api/users")
        assert response.status_code == 200
        assert response.json() == fake_users
