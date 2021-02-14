from passlib.context import CryptContext
from .settings import JWT_SECRET

import jwt

ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    default="bcrypt",
    pbkdf2_sha256__default_rounds=30000
)


def encrypt_password(password: str) -> str:
    """ encrypt password """
    return pwd_context.encrypt(password)


def check_encryption(plain_password: str, hashed: str) -> bool:
    """ return true if plain_password concord with stored hash, else false """
    return pwd_context.verify(plain_password, hashed)


def generate_auth_token(payload: dict) -> str:
    """ encrypt a jwt """
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


def decode_auth_token(token: str) -> dict:
    """ decode a jwt """
    return jwt.decode(token, JWT_SECRET, algorithms=ALGORITHM)
