from fastapi import HTTPException, status


class TokenInvalidException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Токен недействителен!"