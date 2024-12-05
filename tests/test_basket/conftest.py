import pytest

from repositories.product import ProductRepository
from tests.conftest import test_async_session


@pytest.fixture
async def product_repository():
    async with test_async_session() as session:
        yield ProductRepository(session)


@pytest.fixture
async def current_product(product_repository, current_test_admin, admin_data):
    add_data = {
        "product_id": 15,
        "user_id": admin_data.user_id,
        "name": "string",
        "description": "string",
        "price": 1,
        "quantity": 5
    }
    product = await product_repository.create(add_data)
    yield product
    await product_repository.delete(product)

@pytest.fixture
async def product_on_basket(current_product, client):
    add_data = {
        "product_id": current_product.product_id,
        "product_count": 3
    }
    await client.post("/basket", json=add_data)
    yield current_product.product_id