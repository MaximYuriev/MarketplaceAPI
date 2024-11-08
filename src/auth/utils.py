from datetime import datetime, UTC, timedelta

import jwt
import bcrypt

from settings import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH, CRYPT_ALGORITHM


def encode_jwt(
    payload: dict,
    private_key: str = PRIVATE_KEY_PATH.read_text(),
    algorithm: str = CRYPT_ALGORITHM,
    expire_minutes: int = 15
):
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=expire_minutes)
    payload.update(
        exp=expire,
        iat=now
    )
    return jwt.encode(payload, private_key, algorithm=algorithm)


def decode_jwt(
    token: str | bytes,
    public_key: str = PUBLIC_KEY_PATH.read_text(),
    algorithm: str = CRYPT_ALGORITHM
):
    return jwt.decode(token, public_key, algorithms=[algorithm])


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password.decode()


def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

