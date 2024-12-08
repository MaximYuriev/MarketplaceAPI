from fastapi import HTTPException, status


class BasketIsEmpty(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Ваша корзина пуста!")