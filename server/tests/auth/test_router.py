import pytest
from fastapi.testclient import TestClient
from fastapi import status
from src.auth.router import router
from src.auth import services

client = TestClient(router)


def test_login_for_access_token_success(monkeypatch):
    def mock_authenticate_user(username, password):
        return {"username": username}

    def mock_create_access_token(data):
        return "mock_access_token"

    monkeypatch.setattr(services, "authenticate_user", mock_authenticate_user)
    monkeypatch.setattr(services, "create_access_token", mock_create_access_token)

    response = client.post(
        "/token", data={"username": "testuser", "password": "testpassword"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "access_token": "mock_access_token",
        "token_type": "bearer",
    }


def test_login_for_access_token_failure(monkeypatch):
    def mock_authenticate_user(username, password):
        return None

    monkeypatch.setattr(services, "authenticate_user", mock_authenticate_user)

    response = client.post(
        "/token", data={"username": "wronguser", "password": "wrongpassword"}
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == "Incorrect username or password"
