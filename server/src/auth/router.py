from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from .schemas import Token
from ..database.schemas import User
from ..utils.crypto_utils import JWT_ALGORITHM
from ..database import repository_selector
from ..database.repositories import UserRepository
import jwt

app = FastAPI()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    userrepository: UserRepository = repository_selector.get_repository("user")

    try:
        user: User = userrepository.get_user_by_username(form_data.username)
        user.encrypt_password()

        if not user or not user.verify_password(form_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = jwt.encode(
        {"sub": user.username}, user.private_key, algorithm=JWT_ALGORITHM
    )
    return Token(access_token=token_data, token_type="bearer")


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    userrepository: UserRepository = repository_selector.get_repository("user")

    user: User = userrepository.get_user_by_username(form_data.username)
    isverified = user.verify_password(form_data.password)
    if not user or not isverified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = jwt.encode(
        {"sub": user.username}, user.private_key, algorithm=JWT_ALGORITHM
    )
    return Token(access_token=token_data, token_type="bearer")


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: User):
    # Encrypt the user's password
    user.encrypt_password()

    user_data = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.encrypted_password,
        "private_key": user.private_key,  # Store the private key securely
    }

    userrepository: UserRepository = repository_selector.get_repository("user")
    userrepository.add_user(user_data)

    token_data = jwt.encode(
        {"sub": user.username}, user.private_key, algorithm=JWT_ALGORITHM
    )
    token: Token = Token(access_token=token_data, token_type="bearer")

    return token


app.include_router(router)
