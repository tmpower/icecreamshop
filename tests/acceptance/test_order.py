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
async def test_create_order_endpoint_for_user_success(test_user, mocker):
    mocker.patch('app.redis.queue.enqueue', return_value=None)

    user = await test_user
    login_data = {
        'username': user.username,
        'password': 'test_password',
    }

    async with AsyncClient(app=app, base_url='http://test') as test_client:
        response = await test_client.post('/token', data=login_data)
        token = response.json()['access_token']

        response = await test_client.post(
            '/orders',
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
            '/orders',
            json={'address': 'addrr', 'items': [{'flavor': 'something', 'amount': 0}]},
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_order_by_id_endpoint_success(test_user, mocker):
    mocker.patch('app.redis.queue.enqueue', return_value=None)

    user = await test_user
    login_data = {
        'username': user.username,
        'password': 'test_password',
    }

    async with AsyncClient(app=app, base_url='http://test') as test_client:
        response = await test_client.post('/token', data=login_data)
        assert response.status_code == 200
        token = response.json()['access_token']

        response = await test_client.post(
            '/orders',
            json=test_order_obj,
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == 201
        order_id = response.json()['order']['id']

        response = await test_client.get(
            '/orders/' + str(order_id),
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == 200
        assert response.json()['id'] == order_id
        assert response.json()['status'] == 'pending'
