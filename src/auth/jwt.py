from datetime import timedelta, datetime, UTC

import jwt

from auth.config import  EXPIRE_TOKEN_MINUTES
from schemas.token import AccessTokenPayload, RefreshTokenPayload, BaseTokenPayload
from settings import PRIVATE_KEY_PATH, CRYPT_ALGORITHM, PUBLIC_KEY_PATH


class JWT:
    @staticmethod
    def create_jwt(
            payload: BaseTokenPayload | AccessTokenPayload | RefreshTokenPayload,
            private_key: str = PRIVATE_KEY_PATH.read_text(),
            algorithm: str = CRYPT_ALGORITHM,
            expire_minutes: int = EXPIRE_TOKEN_MINUTES,
            expire_timedelta:  timedelta | None = None
    ):
        token_data = payload.model_dump()
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=expire_minutes) if expire_timedelta is None else now + expire_timedelta
        token_data.update(
            exp=expire,
            iat=now
        )
        return jwt.encode(token_data, private_key, algorithm=algorithm)

    @staticmethod
    def parse_jwt(
            token: str,
            public_key: str = PUBLIC_KEY_PATH.read_text(),
            algorithm: str = CRYPT_ALGORITHM,
            verify_signature: bool = True
    ):
        return jwt.decode(token, public_key, algorithms=[algorithm], options={"verify_signature": verify_signature})