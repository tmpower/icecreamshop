import pytest
from httpx import AsyncClient

from app.main import app


test_order_obj = {
    'address': '123 Cream St.',
    'items': [
        {
            'flavor': 'chocolate',
            'amount': 2
        },
        {
            'flavor': 'vanilla',
            'amount': 3
        }
    ]
}


@pytest.mark.asyncio
async def test_create_order_endpoint_for_user_success(test_user):
    user = await test_user
    login_data = {
        'username': user.username,
        'password': 'test_password',
    }

    async with AsyncClient(app=app, base_url='http://test') as test_client:
        response = await test_client.post('/token', data=login_data)
        token = response.json()['access_token']

        response = await test_client.post(
            '/order',
            json=test_order_obj,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == 201
        assert response.json()['message'] == 'order is created, it will be shipped once the payment is successful'
        assert 'order' in response.json()
        assert 'id' in response.json()['order']
        assert response.json()['order']['status'] == 'pending'


@pytest.mark.asyncio
async def test_create_order_endpoint_for_user_fail(test_user):
    user = await test_user
    login_data = {
        'username': user.username,
        'password': 'test_password',
    }

    async with AsyncClient(app=app, base_url='http://test') as test_client:
        response = await test_client.post('/token', data=login_data)
        token = response.json()['access_token']

        response = await test_client.post(
            '/order',
            json={'address': 'addrr', 'items': [{'flavor': 'something', 'amount': 0}]},
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == 422
