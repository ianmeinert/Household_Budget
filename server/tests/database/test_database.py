import pytest
from src.database.factory import RepositoryFactory
from src.database.schemas import User


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
def test_create_user(db_file, user_data):
    rf = RepositoryFactory(db_file).get_user_repository()
    # encrypt the user password
    user: User = rf.add_user(user_data)
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]


@pytest.mark.usefixtures("db_file")
def test_get_user_by_name(db_file, user_data):
    rf = RepositoryFactory(db_file).get_user_repository()
    # encrypt the user password
    user: User = rf.get_user_by_name(user_data["username"])
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
