import pytest
from httpx import AsyncClient

from app.main import app


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
