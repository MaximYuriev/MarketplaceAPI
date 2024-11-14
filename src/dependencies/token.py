from fastapi import Depends
from jwt import InvalidTokenError

from auth.jwt import JWT
from exceptions.token import TokenInvalidException
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
        raise TokenInvalidException

