from logging import getLogger
from typing import AsyncGenerator
from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base


logger = getLogger(__name__)

db_url = getenv('DATABASE_URL')
if db_url is None:
    logger.error('DATABASE_URL not set')
    exit(1)
async_engine = create_async_engine(db_url)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

Base = declarative_base()


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info('database initialized')


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
