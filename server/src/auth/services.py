from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

from ..database.repositories import UserRepository
from . import config
from ..database import repository_selector

user_repository: UserRepository = repository_selector.get_repository("user")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    salt = get_random_bytes(16)
    hashed_password = scrypt(password, salt, 32, N=2**14, r=8, p=1)
    return salt + hashed_password


def authenticate_user(username: str, password: str):
    id, _, _ = user_repository.get_user_by_name(username)
    name, hashed_password = user_repository.get_user_credentials_by_id(id)
    if not id or not verify_password(password, hashed_password):
        return None
    return name


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.now(datetime.timezone.utc) + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt
