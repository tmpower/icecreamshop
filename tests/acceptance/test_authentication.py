from typing import AsyncGenerator

import bcrypt
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.models.user import User
from app.database import Base, get_async_session


@pytest.fixture
async def init_test_db(request: pytest.FixtureRequest) -> AsyncSession:
    async_engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    async_session = async_sessionmaker(async_engine)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def finalize():
        await async_session.close_all()
        await async_engine.dispose()

    request.addfinalizer(finalize)

    return async_session


@pytest.fixture
async def get_test_session(init_test_db) -> AsyncGenerator[AsyncSession, None]:
    async_session = await init_test_db
    async with async_session() as session:
        yield session


@pytest.fixture
async def test_user(get_test_session) -> User:
    async for session in get_test_session:
        app.dependency_overrides[get_async_session] = lambda: session
        test_user = User(
            email='test_user@example.com',
            username='test_user',
            hashed_password=bcrypt.hashpw(b'test_password', bcrypt.gensalt()),
        )
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)
        return test_user


@pytest.mark.asyncio
async def test_login_for_access_token(test_user):
    user = await test_user
    login_data = {
        'username': user.username,
        'password': 'test_password',
    }
    async with AsyncClient(app=app, base_url='http://test') as test_client:
        response = await test_client.post('/token', data=login_data)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'

    # test invalid credentials
    invalid_login_data = {'username': user.username, 'password': 'wrong_password'}
    async with AsyncClient(app=app, base_url='http://test') as test_client:
        response = await test_client.post('/token', data=invalid_login_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_access_protected_user(test_user):
    user = await test_user
    login_data = {
        'username': user.username,
        'password': 'test_password',
    }
    async with AsyncClient(app=app, base_url='http://test') as test_client:
        response = await test_client.post('/token', data=login_data)
        token = response.json()['access_token']
        response = await test_client.get(
            '/protected', headers={'Authorization': f'Bearer {token}'}
        )
    assert response.status_code == 200
    assert 'user' in response.json()
    assert response.json()['user']['email'] == 'test_user@example.com'

    # test invalid token
    async with AsyncClient(app=app, base_url='http://test') as test_client:
        response = await test_client.post('/token', data=login_data)
        token = response.json()['access_token'] + 'wrong'
        response = await test_client.get(
            '/protected', headers={'Authorization': f'Bearer {token}'}
        )
    assert response.status_code == 401
