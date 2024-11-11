from fastapi import Depends, HTTPException
from jwt import InvalidTokenError
from starlette import status


from auth.jwt import JWT
from services.access_token import AccessTokenServices


def current_token_payload(
        access_token_services: AccessTokenServices = Depends()
):
    return get_token_payload(access_token_services)

def current_token_payload_for_refresh(access_token_services: AccessTokenServices = Depends()):
    return get_token_payload(access_token_services, refresh=True)

def get_token_payload(access_token_services: AccessTokenServices, refresh: bool = False):
    token = access_token_services.get_token()
    try:
        return JWT.parse_jwt(token, verify_signature=not refresh)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен!"
        )

