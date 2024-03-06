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


async def update_order_status(order: Order, status: str, session: AsyncSession) -> None:
    order.status = status
    try:
        await session.commit()
    except Exception as e:
        logger.warning(f'failed to update order status in database: {e}')
        await session.rollback()
        raise Exception
    else:
        await session.refresh(order)
        logger.info(f'updated order status in database by username: {order.id}')


async def get_order_by_id(order_id: int, session: AsyncSession) -> Optional[Order]:
    return await session.get(Order, order_id)
