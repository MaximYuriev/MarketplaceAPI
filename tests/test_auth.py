from httpx import AsyncClient


async def test_reg(client: AsyncClient):
    user_create={
        "email": "user@example.com",
        "password": "strings",
        "firstname": "string",
        "surname": "string"
    }
    response = await client.post("/auth/reg", json=user_create)
    body = response.json()
    assert response.status_code == 200
    assert body['detail'] == "Пользователь успешной зарегистрирован!"

async def test_login(client: AsyncClient):
    user_login={
        "email": "user@example.com",
        "password": "strings"
    }
    response = await client.post("/auth/login", json=user_login)
    body = response.json()
    assert response.status_code == 200
    assert body['detail'] == "Пользователь вошел в аккаунт!"

async def test_refresh_token(client: AsyncClient):
    response = await client.get("/auth/refresh")
    body = response.json()
    assert response.status_code == 200
    assert body['detail'] == "Токен обновлен!"

