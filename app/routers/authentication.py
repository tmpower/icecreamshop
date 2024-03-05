from datetime import timedelta
from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.services.authentication import authenticate_user, create_access_token


router = APIRouter()
logger = getLogger(__name__)



@router.post('/token', response_model=dict)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    logger.info(f'login for access token: {form_data.username}')

    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        logger.warning(f'login for access token failed: {form_data.username}')
        raise HTTPException(
            status_code=401,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token(form_data.username)
    if not access_token:
        logger.warning(f'login for access token failed: {form_data.username}')
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while generating token',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return {'access_token': access_token, 'token_type': 'bearer'}
