import jwt
import pytest
from fastapi.testclient import TestClient

from householdbudget.database.factory import RepositoryFactory
from householdbudget.database.schemas import User
from householdbudget.main import app
from householdbudget.utils.crypto_utils import JWT_ALGORITHM

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

    # Verify that the user was added to the database
    rf = RepositoryFactory(db_file).get_user_repository()
    user = rf.get_user_by_username(user_data["username"])
    assert user is not None
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    assert user.password_encryptor.encrypted_password is not None
    assert user.password_encryptor.private_key is not None


@pytest.mark.usefixtures("db_file")
def test_login_user(db_file, user_data):
    rf = RepositoryFactory(db_file).get_user_repository()
    # Add the user to the repository with the required fields
    rf.add_user(user_data)

    user: User = rf.get_user_by_username(user_data["username"])

    response = client.post(
        "/login",
        data=user_data,
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Verify that the token is valid by decoding it
    token = data["access_token"]
    decoded_token = jwt.decode(
        token, user.password_encryptor.private_key, algorithms=[JWT_ALGORITHM]
    )
    assert decoded_token["sub"] == user_data["username"]
