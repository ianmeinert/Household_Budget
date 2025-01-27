import pytest
from src.database.factory import RepositoryFactory


@pytest.fixture
def user_data():
    return {
        "name": "testuser",
        "password": "hashedpassword",
        "email": "test_me@testemail.com",
    }


@pytest.mark.usefixtures("db_file")
def test_create_user(db_file, user_data):
    rf = RepositoryFactory(db_file).get_user_repository()
    _, name, email = rf.add_user(user_data)
    assert name == user_data["name"]
    assert email == user_data["email"]


@pytest.mark.usefixtures("db_file")
def test_get_user_by_name(db_file, user_data):
    rf = RepositoryFactory(db_file).get_user_repository()
    _, name, email = rf.get_user_by_name(user_data["name"])
    assert name == user_data["name"]
    assert email == user_data["email"]
