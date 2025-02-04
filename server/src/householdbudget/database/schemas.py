import base64

from pydantic import BaseModel

from ..utils.crypto_utils import decrypt, encrypt, generate_keys


class User(BaseModel):
    id: int = None
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    encrypted_password: bytes = None
    private_key: bytes = None
    cyphertext: bytes = None

    def encrypt_password(self):
        public_key, self.private_key = generate_keys()
        c, encrypted_text = encrypt(self.password, public_key)
        self.cyphertext = base64.urlsafe_b64encode(c)
        self.encrypted_password = base64.urlsafe_b64encode(encrypted_text)
        self.password = str()  # Clear the password

    def decrypt_password(self):
        if self.private_key is None:
            raise ValueError("Private key is not available for decryption.")
        # Decode the values
        c = base64.urlsafe_b64decode(self.cyphertext)
        encrypted_text = base64.urlsafe_b64decode(self.encrypted_password)
        decrypted = decrypt(c, encrypted_text, self.private_key)
        return decrypted

    def verify_password(self, password: str) -> bool:
        decrypted = self.decrypt_password()
        return decrypted == password

    class ConfigDict:
        # Ensure sensitive fields are not exposed
        fields = {
            "private_key": {"exclude": True},
            "encrypted_password": {"exclude": True},
        }
