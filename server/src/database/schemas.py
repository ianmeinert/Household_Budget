from pydantic import BaseModel

from ..utils.crypto_utils import generate_keys, encrypt, decrypt


class User(BaseModel):
    id: int = None
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    encrypted_password: str = None
    private_key: bytes = None
    cyphertext: bytes = None

    def encrypt_password(self):
        public_key, self.private_key = generate_keys()
        self.cyphertext, self.encrypted_password = encrypt(self.password, public_key)
        self.password = str()  # Clear the password

    def decrypt_password(self):
        if self.private_key is None:
            raise ValueError("Private key is not available for decryption.")

        return decrypt(self.cyphertext, self.encrypted_password, self.private_key)

    def verify_password(self, password: str) -> bool:
        decrypted = self.decrypt_password()
        return decrypted == password

    class ConfigDict:
        # Ensure sensitive fields are not exposed
        fields = {
            "private_key": {"exclude": True},
            "encrypted_password": {"exclude": True},
        }
