from httpx import AsyncClient


async def test_add_by_user(product: dict, client: AsyncClient, current_test_user: AsyncClient.cookies):
    response = await client.post("/product/add", json=product, cookies=current_test_user)
    body = response.json()
    assert response.status_code == 403
    assert body['detail'] == "Нет доступа!"


async def test_add_by_admin(product: dict, client: AsyncClient, current_test_admin: AsyncClient.cookies):
    response = await client.post("/product/add", json=product, cookies=current_test_admin)
    body = response.json()
    assert response.status_code == 200
    assert body['detail'] == "Товар добавлен!"


async def test_add_twice(product: dict, client: AsyncClient, current_test_admin: AsyncClient.cookies):
    product.update(name="product")

    response = await client.post("/product/add", json=product, cookies=current_test_admin)
    body = response.json()
    assert response.status_code == 200
    assert body['detail'] == "Товар добавлен!"

    response = await client.post("/product/add", json=product, cookies=current_test_admin)
    body = response.json()
    assert response.status_code == 400
    assert body['detail'] == "Товар уже существует!"
