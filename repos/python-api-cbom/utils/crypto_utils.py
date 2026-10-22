import hashlib
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


# SHA-256: Modern hashing
def sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


# AES-256-GCM: Modern authenticated encryption
def aes_demo(text):
    key = AESGCM.generate_key(bit_length=256)
    nonce = secrets.token_bytes(12)
    aes = AESGCM(key)

    encrypted = aes.encrypt(nonce, text.encode(), None)
    decrypted = aes.decrypt(nonce, encrypted, None)

    return decrypted.decode()


# RSA-2048: Digital signature
def rsa_demo(text):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    signature = private_key.sign(
        text.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    private_key.public_key().verify(
        signature,
        text.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    return True


# PBKDF2-SHA256: Password-based key derivation
def pbkdf2_demo(password):
    salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac(
        'sha256', password.encode(), salt, 120000
    )
    return key.hex()
