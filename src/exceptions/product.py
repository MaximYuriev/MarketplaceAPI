from fastapi import HTTPException, status


class ProductNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден!")


class ProductAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Товар уже существует!")


class ProductNameNotUnique(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Название товара занято!")


class ProductNotInStock(HTTPException):
    def __init__(self, product_name: str = ""):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Товар {product_name !r} не в наличии!")


class ProductQuantityException(HTTPException):
    def __init__(self, product_name: str = ""):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Количество добавляемого товара {product_name !r} больше, чем имеется в наличии!"
        )


class ProductAlreadyInBasket(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Товар уже добавлен в корзину!")


class ProductNotInBasket(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден в корзине!")
