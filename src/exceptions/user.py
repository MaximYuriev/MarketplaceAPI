from fastapi import HTTPException, status


class UserNotAuthorized(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован!")

class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.status.HTTP_404_NOT_FOUND, detail="Пользователь не найден!")

class UserAccessException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа!")

class UserValidateError(HTTPException):
    def __init__(self):
        super().__init__(status.HTTP_403_FORBIDDEN, detail="Неверный логин или пароль!")

class UserEmailNotUnique(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Электронная почта занята!")