from json import dumps
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.user import User
from app.redis import queue
from app.repositories.order import create_order
from app.services.payment import make_payment
from app.services.stats import update_stats


async def place_order(order_dict: dict, user: User, session: AsyncSession) -> Optional[Order]:
    order_full = order_dict.copy()
    order_full.update({'user_id': user.id})
    order_full['items'] = dumps(order_dict['items'])
    order_model = Order(**order_full)
    order = await create_order(order_model, session)

    # make the payment in the separate process
    queue.enqueue(make_payment, order.id)

    await update_stats(order_dict['items'], session)

    return order
