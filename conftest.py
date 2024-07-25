import pytest
from faker import Faker
import requests
from data import Urls

faker = Faker()


@pytest.fixture
def new_user_data():
    return {
        "email": faker.email(),
        "password": faker.password(),
        "name": faker.name()
    }


@pytest.fixture
def new_user(new_user_data):
    response = requests.post(Urls.REGISTER_URL, json=new_user_data)
    response_data = response.json()

    return new_user_data, response_data['accessToken']


@pytest.fixture
def refresh_token(new_user_data):
    response = requests.post(Urls.REGISTER_URL, json=new_user_data)
    response_data = response.json()

    return response_data.get('refreshToken')


@pytest.fixture
def delete_user():
    def _delete_user(access_token):
        headers = {
            "Authorization": access_token
        }
        response = requests.delete(Urls.USER_DELETE_URL, headers=headers)
        return response.status_code

    return _delete_user


@pytest.fixture
def valid_ingredient_ids():
    response = requests.get(Urls.INGREDIENTS_URL)
    ingredients = response.json()
    return [ingredient['_id'] for ingredient in ingredients['data'] if ingredient['_id']]


@pytest.fixture
def setup_orders(new_user):
    _, access_token = new_user
    orders = []
    for _ in range(3):
        order_data = {
            "ingredients": [
                "61c0c5a71d1f82001bdaaa78",
                "61c0c5a71d1f82001bdaaa7a"
            ]
        }
        headers = {
            "Authorization": access_token
        }
        order_response = requests.post(Urls.ORDERS_URL, json=order_data, headers=headers)
        order_response_data = order_response.json()

        orders.append(order_response_data['order'])

    return orders
