import datetime
import unittest
from unittest.mock import patch, MagicMock
from src.auth.services import (
    verify_password,
    get_password_hash,
    authenticate_user,
    create_access_token,
)


class TestAuthServices(unittest.TestCase):
    @patch("src.auth.services.pwd_context.verify")
    def test_verify_password(self, mock_verify):
        mock_verify.return_value = True
        self.assertTrue(verify_password("plain_password", "hashed_password"))
        mock_verify.assert_called_once_with("plain_password", "hashed_password")

    @patch("src.auth.services.scrypt")
    @patch("src.auth.services.get_random_bytes")
    def test_get_password_hash(self, mock_get_random_bytes, mock_scrypt):
        mock_get_random_bytes.return_value = b"random_salt"
        mock_scrypt.return_value = b"hashed_password"
        result = get_password_hash("password")
        self.assertEqual(result, b"random_salt" + b"hashed_password")
        mock_get_random_bytes.assert_called_once_with(16)
        mock_scrypt.assert_called_once_with(
            "password", b"random_salt", 32, N=2**14, r=8, p=1
        )

    @patch("src.auth.services.user_repository.get_user_by_name")
    @patch("src.auth.services.user_repository.get_user_credentials_by_id")
    @patch("src.auth.services.verify_password")
    def test_authenticate_user(
        self,
        mock_verify_password,
        mock_get_user_credentials_by_id,
        mock_get_user_by_name,
    ):
        mock_get_user_by_name.return_value = (1, "username", "email")
        mock_get_user_credentials_by_id.return_value = ("username", "hashed_password")
        mock_verify_password.return_value = True
        result = authenticate_user("username", "password")
        self.assertEqual(result, "username")
        mock_get_user_by_name.assert_called_once_with("username")
        mock_get_user_credentials_by_id.assert_called_once_with(1)
        mock_verify_password.assert_called_once_with("password", "hashed_password")

    @patch("src.auth.services.jwt.encode")
    @patch("src.auth.services.datetime")
    def test_create_access_token(self, mock_datetime, mock_jwt_encode):
        mock_datetime.timezone.utc = datetime.timezone.utc
        mock_datetime.now.return_value = datetime.datetime(
            2023, 1, 1, tzinfo=datetime.timezone.utc
        )
        mock_jwt_encode.return_value = "encoded_jwt"
        data = {"sub": "username"}
        expires_delta = datetime.timedelta(minutes=15)
        result = create_access_token(data, expires_delta)
        self.assertEqual(result, "encoded_jwt")
        mock_jwt_encode.assert_called_once()
        mock_datetime.now.assert_called_once_with(datetime.timezone.utc)


if __name__ == "__main__":
    unittest.main()
