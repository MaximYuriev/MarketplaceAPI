from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from settings import POSTGRES_DB, POSTGRES_PASSWORD,POSTGRES_PORT,POSTGRES_HOST,POSTGRES_USER


Base = declarative_base()

db_url = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
db_engine = create_async_engine(db_url, echo=False)
async_session = async_sessionmaker(db_engine, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session