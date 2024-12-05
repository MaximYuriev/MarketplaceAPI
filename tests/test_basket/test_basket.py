from httpx import AsyncClient


async def test_add_product_on_basket(current_product, client: AsyncClient):
    add_data = {
        "product_id": current_product.product_id,
        "product_count": 3
    }
    response = await client.post("/basket", json=add_data)
    body = response.json()
    assert response.status_code == 200
    assert body["detail"] == "Товар успешно добавлен в корзину!"


async def test_update_product_on_basket(product_on_basket, client: AsyncClient):
    update_data = {
        "product_count": "4"
    }
    response = await client.put(f"/basket/{product_on_basket}", json=update_data)
    body = response.json()
    assert response.status_code == 200
    assert body["detail"] == "Товар в корзине успешно изменен!"


async def test_delete_product_on_basket(product_on_basket, client: AsyncClient):
    response = await client.delete(f"/basket/{product_on_basket}")
    body = response.json()
    assert response.status_code == 200
    assert body["detail"] == "Товар успешно удален!"
