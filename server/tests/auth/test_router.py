import pytest
from fastapi.testclient import TestClient

from src.auth.router import app
from src.database.factory import RepositoryFactory

client = TestClient(app)


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "email": "test_me@testemail.com",
        "password": "cleanpassword",
    }


@pytest.mark.usefixtures("db_file")
def test_register_user(db_file, user_data):
    response = client.post("/register", json=user_data)
    assert response.status_code == 201
    data = response.json()

    assert data["token_type"] == "bearer"
    assert "access_token" in data


@pytest.mark.usefixtures("db_file")
def test_login_user(db_file, user_data):
    rf = RepositoryFactory(db_file).get_user_repository()
    rf.add_user(user_data)

    response = client.post("/login", data=user_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
