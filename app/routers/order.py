from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.repositories.order import get_order_by_id
from app.schemas.order import OrderCreateIcecream, OrderResponseIceCream
from app.services.order import place_order
from app.services.authentication import get_current_user, oauth2_scheme


router = APIRouter()
logger = getLogger(__name__)


@router.post('/orders', response_model=dict, status_code=201)
async def create_order_endpoint(
    order: OrderCreateIcecream,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
):
    current_user = await get_current_user(token, session)
    logger.info(f'order made by: {current_user.username}')

    failed_exception = HTTPException(
        status_code=400,
        detail='Could not create the order',
    )
    try:
        order = await place_order(order.to_dict(), current_user, session)
    except Exception as e:
        logger.warning(f'failed to create order: {e}')
        raise failed_exception

    return {
        'order': OrderResponseIceCream(id=order.id, status=order.status),
        'message': 'order is created, it will be shipped once the payment is successful',
    }


@router.get('/orders/{order_id}', response_model=OrderResponseIceCream)
async def get_order_endpoint(
    order_id: int,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
):
    order = await get_order_by_id(order_id, session)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    current_user = await get_current_user(token, session)
    if current_user.id != order.user_id:
        raise HTTPException(status_code=403, detail='Does not have an access to the resource')

    return {
        'id': order.id,
        'status': order.status,
    }
