import pytest
from fastapi.testclient import TestClient
from src.auth.router import app
from src.database.factory import RepositoryFactory
from src.database.schemas import User

client = TestClient(app)


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "email": "test_me@testemail.com",
        "password": "hashedpassword",
        "private_key": "privatekey123",
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
    rf_data = rf.add_user(user_data)
    print(rf_data.model_dump())
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"],
    }
    response = client.post("/login", data=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
