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
async def test_create_order_and_get_stats(test_user, mocker):
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
        response = await test_client.post(
            '/orders',
            json=test_order_obj,
            headers={'Authorization': f'Bearer {token}'},
        )

        response = await test_client.get('/stats')
        assert response.status_code == 200
        assert response.json()[0]['flavor'] == 'chocolate'
        assert response.json()[0]['count'] == 4
        assert response.json()[1]['flavor'] == 'vanilla'
        assert response.json()[1]['count'] == 6
