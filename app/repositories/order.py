from logging import getLogger
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order


logger = getLogger(__name__)


async def create_order(order: Order, session: AsyncSession) -> Optional[Order]:
    try:
        session.add(order)
        await session.commit()
    except Exception as e:
        logger.warning(f'failed to create order in database: {e}')
        await session.rollback()
        raise Exception
    else:
        await session.refresh(order)
        logger.info(f'created order in database by username: {order.id}')

    return order
