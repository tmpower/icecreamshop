from logging import getLogger
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


logger = getLogger(__name__)


async def get_user_by_username(username: str, session: AsyncSession) -> Optional[User]:
    logger.info(f'get user from database by username: {username}')
    query_str = select(User).filter(User.username == username)
    result = await session.execute(query_str)
    user = result.scalars().first()
    return user
