from fastapi import HTTPException, status

from auth.config import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE


class TokenInvalidException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен недействителен!")

class TokenNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Токен не найден!")

class TokenTypeException(HTTPException):
    def __init__(self, received_token_type: str = REFRESH_TOKEN_TYPE, waited_token_type: str = ACCESS_TOKEN_TYPE):
        detail = f"Неверный тип токена: {received_token_type !r}! Ожидаемый тип - {waited_token_type !r}"
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
