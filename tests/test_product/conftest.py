import pytest


@pytest.fixture
def product():
    product = {
        "name": "string",
        "description": "string",
        "price": 1,
        "quantity": 1
    }
    return product
