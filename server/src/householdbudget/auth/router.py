import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..database import repository_selector
from ..database.exceptions import RecordNotFoundError
from ..database.repositories import UserRepository
from ..database.schemas import User
from ..utils.crypto_utils import JWT_ALGORITHM
from .schemas import PasswordEncryptor, Token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    userrepository: UserRepository = repository_selector.get_repository("user")

    try:
        user: User = userrepository.get_user_by_username(form_data.username)
        encryption_data = userrepository.get_encryption_data(user.id)
        user.password_encryptor = PasswordEncryptor(**encryption_data)

        if not user or not user.verify_password(form_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except RecordNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    token_data = jwt.encode(
        {"sub": user.username},
        user.password_encryptor.private_key,
        algorithm=JWT_ALGORITHM,
    )
    return Token(access_token=token_data, token_type="bearer")


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    userrepository: UserRepository = repository_selector.get_repository("user")

    try:
        user: User = userrepository.get_user_by_username(form_data.username)
        encryption_data = userrepository.get_encryption_data(user.id)
        user.password_encryptor = PasswordEncryptor(**encryption_data)
        isverified = user.verify_password(form_data.password)

        if not user or not isverified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except RecordNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    token_data = jwt.encode(
        {"sub": user.username},
        user.password_encryptor.private_key,
        algorithm=JWT_ALGORITHM,
    )
    return Token(access_token=token_data, token_type="bearer")


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: User):
    # Encrypt the user's password
    user.set_password(user.password)

    user_data = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
    }

    userrepository: UserRepository = repository_selector.get_repository("user")
    userrepository.add_user(user_data)

    # Retrieve the user to get the assigned ID
    user = userrepository.get_user_by_username(user.username)

    token_data = jwt.encode(
        {"sub": user.username},
        user.password_encryptor.private_key,
        algorithm=JWT_ALGORITHM,
    )
    token: Token = Token(access_token=token_data, token_type="bearer")

    return token
