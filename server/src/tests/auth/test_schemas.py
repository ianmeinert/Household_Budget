import unittest

from householdbudget.auth.schemas import PasswordEncryptor
from householdbudget.database.schemas import User


class TestUserSchema(unittest.TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "securepassword123",
        }

    def test_set_password(self):
        user = User(**self.user_data)
        user.set_password(self.user_data["password"])
        self.assertIsNotNone(user.password_encryptor.encrypted_password)
        self.assertIsNotNone(user.password_encryptor.private_key)
        self.assertEqual(user.password, "")

    def test_decrypt_password(self):
        user = User(**self.user_data)
        user.set_password(self.user_data["password"])
        decrypted_password = user.password_encryptor.decrypt_password()
        self.assertEqual(decrypted_password, self.user_data["password"])

    def test_verify_password(self):
        user = User(**self.user_data)
        user.set_password(self.user_data["password"])
        self.assertTrue(user.verify_password(self.user_data["password"]))
        self.assertFalse(user.verify_password("wrongpassword"))

    def test_password_encryptor_initialization(self):
        password_encryptor = PasswordEncryptor()
        self.assertIsNone(password_encryptor.encrypted_password)
        self.assertIsNone(password_encryptor.private_key)
        self.assertIsNone(password_encryptor.cyphertext)
        self.assertIsNone(password_encryptor.salt)

    def test_password_encryptor_encryption(self):
        password_encryptor = PasswordEncryptor()
        password = "securepassword123"
        password_encryptor.encrypt_password(password)
        self.assertIsNotNone(password_encryptor.encrypted_password)
        self.assertIsNotNone(password_encryptor.private_key)
        self.assertIsNotNone(password_encryptor.cyphertext)
        self.assertIsNotNone(password_encryptor.salt)

    def test_password_encryptor_decryption(self):
        password_encryptor = PasswordEncryptor()
        password = "securepassword123"
        password_encryptor.encrypt_password(password)
        decrypted_password = password_encryptor.decrypt_password()
        self.assertEqual(decrypted_password, password)


if __name__ == "__main__":
    unittest.main()
