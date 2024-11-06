from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from models.user import UserRole



@asynccontextmanager #При каждом запуске приложения будет происходить проверка на наличие нужных ролей в базе данных
async def lifespan(_:FastAPI):
    await UserRole.create_default_roles()
    yield


app = FastAPI(title="Marketplace API", lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)