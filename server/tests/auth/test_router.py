from fastapi.testclient import TestClient
from src.auth.router import app

client = TestClient(app)


def test_login_success():
    response = client.post(
        "/token", json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_failure():
    response = client.post(
        "/token", json={"username": "wronguser", "password": "wrongpassword"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid credentials"}


def test_read_secure_data():
    # First, login to get the token
    login_response = client.post(
        "/token", json={"username": "testuser", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]

    # Use the token to access the secure endpoint
    response = client.get("/secure-data", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "This is secured data."}
