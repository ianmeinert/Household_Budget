import unittest

from householdbudget.utils.crypto_utils import decrypt, encrypt, generate_keys


class TestCryptoUtils(unittest.TestCase):
    def test_generate_keys(self):
        public_key, private_key = generate_keys()
        self.assertIsNotNone(public_key)
        self.assertIsNotNone(private_key)

    def test_encrypt_decrypt(self):
        public_key, private_key = generate_keys()
        phrase = "This is a test phrase."
        ciphertext, encrypted_text = encrypt(phrase, public_key)
        self.assertIsNotNone(ciphertext)
        self.assertIsNotNone(encrypted_text)

        decrypted_phrase = decrypt(ciphertext, encrypted_text, private_key)
        self.assertEqual(phrase, decrypted_phrase)


if __name__ == "__main__":
    unittest.main()
