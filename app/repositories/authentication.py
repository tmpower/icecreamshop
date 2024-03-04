from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_user_by_username(username: str, session: AsyncSession) -> Optional[User]:
    query_str = select(User).filter(User.username == username)
    result = await session.execute(query_str)
    user = result.scalars().first()
    return user
