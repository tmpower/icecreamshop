from typing import AsyncGenerator
from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base


async_engine = create_async_engine(getenv('DATABASE_URL'), echo=True)
async_session = async_sessionmaker(async_engine)

Base = declarative_base()


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
