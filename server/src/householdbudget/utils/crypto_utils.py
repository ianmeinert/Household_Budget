import base64
import hashlib
import os

from cryptography.fernet import Fernet
from kyber_py.kyber import Kyber1024

JWT_ALGORITHM = "HS256"


def generate_keys():
    """Generate a public/private key pair."""
    pk, sk = Kyber1024.keygen()
    return pk, sk


def encrypt(plaintext, pk):
    key, c = Kyber1024.encaps(pk)

    # Generate a random salt
    salt = os.urandom(16)

    # Derive a Fernet-compatible key from the Kyber shared key
    fernet_key = base64.urlsafe_b64encode(
        hashlib.pbkdf2_hmac("sha256", key, salt, 100000)
    )

    # Use the derived key to encrypt the plaintext
    fernet = Fernet(fernet_key)
    encrypted_text = fernet.encrypt(plaintext.encode())

    return c, salt, encrypted_text


def decrypt(ciphertext, salt, encrypted_text, private_key):
    # Decrypt the ciphertext to retrieve the key
    key = Kyber1024.decaps(private_key, ciphertext)

    # Derive the Fernet-compatible key from the Kyber shared keypy
    fernet_key = base64.urlsafe_b64encode(
        hashlib.pbkdf2_hmac("sha256", key, salt, 100000)
    )

    # Use the derived key to decrypt the encrypted text
    fernet = Fernet(fernet_key)
    decrypted_text = fernet.decrypt(encrypted_text).decode()

    return decrypted_text
