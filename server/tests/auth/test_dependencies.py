import pytest
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from unittest.mock import patch, MagicMock
import src.auth.dependencies
from src.auth.dependencies import get_current_user
from src.auth import config, schemas
from src.database import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def test_get_current_user_valid_token():
    token = "valid_token"
    payload = {"sub": "testuser"}
    user = MagicMock()
    user.username = "testuser"

    with patch("src.auth.dependencies.jwt.decode", return_value=payload):
        with patch(
            "src.auth.dependencies.repository_selector.get_repository"
        ) as mock_repo_selector:
            mock_repo = MagicMock(UserRepository)
            mock_repo.get_user_by_name.return_value = user
            mock_repo_selector.return_value = mock_repo

            result = get_current_user(token)
            assert result == user


def test_get_current_user_invalid_token():
    token = "invalid_token"

    with patch("src.auth.dependencies.jwt.decode", side_effect=JWTError):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Could not validate credentials"


def test_get_current_user_no_username_in_token():
    token = "valid_token"
    payload = {"sub": None}

    with patch("src.auth.dependencies.jwt.decode", return_value=payload):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Could not validate credentials"


def test_get_current_user_user_not_found():
    token = "valid_token"
    payload = {"sub": "testuser"}

    with patch("src.auth.dependencies.jwt.decode", return_value=payload):
        with patch(
            "src.auth.dependencies.repository_selector.get_repository"
        ) as mock_repo_selector:
            mock_repo = MagicMock(UserRepository)
            mock_repo.get_user_by_name.return_value = None
            mock_repo_selector.return_value = mock_repo

            with pytest.raises(HTTPException) as exc_info:
                get_current_user(token)
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "Could not validate credentials"
