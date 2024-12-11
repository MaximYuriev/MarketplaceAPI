from contextlib import asynccontextmanager
import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).resolve().parent.parent))
from models.user import UserRole
from routers.user import user_router
from routers.auth import auth_router
from routers.product import product_router
from routers.basket import basket_router
from routers.order import order_router
from routers.wallet import wallet_router


@asynccontextmanager  # При каждом запуске приложения будет происходить проверка на наличие нужных ролей в базе данных
async def lifespan(_: FastAPI):
    await UserRole.create_default_roles()
    yield


app = FastAPI(title="Marketplace API", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(user_router)
app.include_router(wallet_router)
app.include_router(basket_router)
app.include_router(order_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
