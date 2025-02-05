import base64

from pydantic import BaseModel

from ..utils.crypto_utils import decrypt, encrypt, generate_keys


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordEncryptor(BaseModel):
    encrypted_password: bytes = None
    private_key: bytes = None
    cyphertext: bytes = None
    salt: bytes = None

    def encrypt_password(self, password: str):
        public_key, self.private_key = generate_keys()
        c, self.salt, encrypted_text = encrypt(password, public_key)
        self.cyphertext = base64.urlsafe_b64encode(c)
        self.encrypted_password = base64.urlsafe_b64encode(encrypted_text)

    def decrypt_password(self):
        if self.private_key is None:
            raise ValueError("Private key is not available for decryption.")
        # Decode the values
        c = base64.urlsafe_b64decode(self.cyphertext)
        encrypted_text = base64.urlsafe_b64decode(self.encrypted_password)
        decrypted = decrypt(c, self.salt, encrypted_text, self.private_key)
        return decrypted
