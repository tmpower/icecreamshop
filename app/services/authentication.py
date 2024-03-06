from datetime import datetime, timedelta
from logging import getLogger
from os import getenv
from typing import Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.user import User as UserModel
from app.repositories.authentication import get_user_by_username


logger = getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def authenticate_user(
    username: str, password: str, db: AsyncSession
) -> Optional[UserModel]:
    user = await get_user_by_username(username, db)
    if not user:
        logger.info(f'user not found: {username}')
        return None
    if not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
        logger.info(f'wrong password for user: {username}')
        return None
    return user


def create_access_token(username: str) -> Optional[str]:
    to_encode = {'sub': username}
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        logger.warning(f'failed to encode with JWT: {e}')
        return None
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_session)
) -> Optional[UserModel]:
    logger.info(f'get current user from token')
    credentials_exception = HTTPException(
        status_code=401,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            logger.warning(f'attemped to access without valid token')
            raise credentials_exception
        # check if the token is expired
        if 'exp' in payload:
            expiration = datetime.fromtimestamp(payload['exp'])
            if expiration <= datetime.utcnow():
                logger.warning(f'attemped to access without valid token')
                raise credentials_exception
    except jwt.PyJWTError:
        logger.warning(f'attemped to access without valid token')
        raise credentials_exception
    user = await get_user_by_username(username, db)
    if user is None:
        logger.warning(f'attemped to access without valid token')
        raise credentials_exception
    return user
