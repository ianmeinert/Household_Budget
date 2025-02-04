import base64
import hashlib

from cryptography.fernet import Fernet
from kyber_py.kyber import Kyber1024

JWT_ALGORITHM = "HS256"  # confirm jwt capability


def generate_keys():
    """Generate a public/private key pair."""
    pk, sk = Kyber1024.keygen()
    return pk, sk


def encrypt(plaintext, pk):
    key, c = Kyber1024.encaps(pk)

    # Derive a Fernet-compatible key from the Kyber shared key
    fernet_key = base64.urlsafe_b64encode(hashlib.sha256(key).digest())

    # Use the derived key to encrypt the plaintext
    fernet = Fernet(fernet_key)
    encrypted_text = fernet.encrypt(plaintext.encode())

    return c, encrypted_text


def decrypt(ciphertext, encrypted_text, private_key):
    # Decrypt the ciphertext to retrieve the key
    key = Kyber1024.decaps(private_key, ciphertext)

    # Derive the Fernet-compatible key from the Kyber shared keypy
    fernet_key = base64.urlsafe_b64encode(hashlib.sha256(key).digest())

    # Use the derived key to decrypt the encrypted text
    fernet = Fernet(fernet_key)
    decrypted_text = fernet.decrypt(encrypted_text).decode()

    return decrypted_text
