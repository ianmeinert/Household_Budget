from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from kyber import Kyber512  # Importing the Kyber512 class from kyber-py
from .schemas import User, Token

app = FastAPI()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to encrypt the password using Kyber
def encrypt_password(password: str) -> str:
    # Generate a key pair using Kyber
    public_key, private_key = Kyber512.keygen()

    # Encrypt the password
    encapsulated_key, shared_secret = Kyber512.enc(public_key)

    # Here you would typically store the encapsulated_key and shared_secret securely
    # For demonstration, we return the encapsulated key in hexadecimal format
    return encapsulated_key.hex()


@router.post("/token", response_model=Token)
async def login(user: User):
    # Encrypt the user's password
    encrypted_password = encrypt_password(user.password)

    # Here you would typically verify the username and encrypted password
    # For demonstration, we assume the user is valid
    if user.username == "testuser":  # Replace with actual user validation
        return {"access_token": encrypted_password, "token_type": "bearer"}

    raise HTTPException(status_code=400, detail="Invalid credentials")


@router.get("/secure-data")
async def read_secure_data(token: str = Depends(oauth2_scheme)):
    # Here you would typically decode and verify the token
    # For demonstration, we assume the token is valid
    return {"message": "This is secured data."}


app.include_router(router)
