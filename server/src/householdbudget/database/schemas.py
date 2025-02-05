from pydantic import BaseModel

from ..auth.schemas import PasswordEncryptor


class User(BaseModel):
    id: int = None
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    password_encryptor: PasswordEncryptor = PasswordEncryptor()

    def set_password(self, password: str):
        self.password_encryptor.encrypt_password(password)
        self.password = str()

    def verify_password(self, password: str) -> bool:
        decrypted = self.password_encryptor.decrypt_password()
        return decrypted == password

    class ConfigDict:
        # Ensure sensitive fields are not exposed
        fields = {
            "password": {"exclude": True},
            "password_encryptor.private_key": {"exclude": True},
            "password_encryptor.encrypted_password": {"exclude": True},
            "password_encryptor.salt": {"exclude": True},
        }
