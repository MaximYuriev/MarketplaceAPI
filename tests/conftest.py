import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
from db import Base, get_session
from src.main import app

db_url_test = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

test_db_engine = create_async_engine(db_url_test, echo=False, poolclass=NullPool)
test_async_session = async_sessionmaker(test_db_engine, expire_on_commit=False)

async def override_get_session():
    async with test_async_session() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

async def create_roles():
    async with test_db_engine.begin() as conn:
        stmt = """INSERT INTO role VALUES (1, 'Администратор'), (2, 'Пользователь')"""
        await conn.execute(text(stmt))

@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    assert POSTGRES_DB == "markettest"
    async with test_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await create_roles()
    yield
    async with test_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
