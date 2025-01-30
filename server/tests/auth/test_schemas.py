import unittest
from src.database.schemas import User


class TestUserSchema(unittest.TestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "securepassword123",
        }

    def test_encrypt_password(self):
        user = User(**self.user_data)
        user.encrypt_password()
        self.assertIsNotNone(user.encrypted_password)
        self.assertIsNotNone(user.private_key)
        self.assertIs(user.__dict__.get("password"), str())

    def test_decrypt_password(self):
        user = User(**self.user_data)
        user.encrypt_password()
        decrypted_password = user.decrypt_password()
        self.assertEqual(decrypted_password, self.user_data["password"])

    def test_verify_password(self):
        user = User(**self.user_data)
        user.encrypt_password()
        self.assertTrue(user.verify_password(self.user_data["password"]))
        self.assertFalse(user.verify_password("wrongpassword"))


if __name__ == "__main__":
    unittest.main()
