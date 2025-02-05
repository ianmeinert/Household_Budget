import pytest

from householdbudget.database.factory import RepositoryFactory
from householdbudget.database.schemas import User


@pytest.fixture
def user_data():
    return {
        "username": "testuser2",
        "first_name": "Test",
        "last_name": "User",
        "email": "test_me2@testemail.com",
        "password": "securepassword123",
    }


@pytest.mark.usefixtures("db_file")
def test_create_user(db_file, user_data):
    rf = RepositoryFactory(db_file).get_user_repository()
    # Add the user and encrypt the password
    user: User = rf.add_user(user_data)
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    assert user.password_encryptor.encrypted_password is not None
    assert user.password_encryptor.private_key is not None


@pytest.mark.usefixtures("db_file")
def test_get_user_by_name(db_file, user_data):
    rf = RepositoryFactory(db_file).get_user_repository()
    rf.add_user(user_data)
    # Retrieve the user by username
    user: User = rf.get_user_by_name(user_data["username"])
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    assert user.password_encryptor.encrypted_password is not None
    assert user.password_encryptor.private_key is not None
