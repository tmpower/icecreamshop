import asyncio
from logging import getLogger

from paymock import pay as paymock_pay
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.order import Order, OrderStatus
from app.repositories.order import update_order_status


logger = getLogger(__name__)


async def update_status(order_id: int, status: str):
    async with async_session() as session:
        order = await session.get(Order, order_id)
        await update_order_status(order, status, session)


def make_payment(order_id: int) -> None:
    logger.info(f'payment processing started for order: {order_id}')

    response = paymock_pay()
    if response == 'success':
        logger.info(f'payment successful for order: {order_id}')
        asyncio.run(update_status(order_id, OrderStatus.paid))
        # TODO: shipment service should handle the shipment
    else:
        logger.warning(f'payment unsuccessful for order: {order_id}')
        asyncio.run(update_status(order_id, OrderStatus.failed))
        # TODO: notification service should send email to the user about payment failure
