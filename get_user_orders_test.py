import unittest
import allure
import requests
from faker import Faker
from data import Urls

fake = Faker()


class TestGetUserOrders(unittest.TestCase):
    tokens = {
        "accessToken": "",
        "refreshToken": ""
    }

    @classmethod
    def setUpClass(cls):
        cls.new_user_data = {
            "email": fake.email(),
            "password": fake.password(),
            "name": fake.name()
        }
        response = requests.post(Urls.REGISTER_URL, json=cls.new_user_data)
        response_data = response.json()
        assert response.status_code == 200 and response_data.get('success') is True
        cls.tokens['accessToken'] = response_data['accessToken']
        cls.tokens['refreshToken'] = response_data['refreshToken']

        cls.orders = []
        for _ in range(3):
            order_data = {
                "ingredients": [
                    "61c0c5a71d1f82001bdaaa78",
                    "61c0c5a71d1f82001bdaaa7a"
                ]
            }
            headers = {
                "authorization": cls.tokens['accessToken']
            }
            order_response = requests.post(Urls.ORDERS_URL, json=order_data, headers=headers)
            order_response_data = order_response.json()
            assert order_response.status_code == 200 and order_response_data.get('success') is True
            cls.orders.append(order_response_data['order'])

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_user_orders(self):
        headers = {"authorization": self.tokens['accessToken']}
        response = requests.get(Urls.ORDERS_URL, headers=headers)
        response_data = response.json()

        assert (response.status_code == 200 and response_data.get('success') is True and 'orders' in response_data and
                len(response_data['orders']) == 3)

    @allure.title('Получение заказов неавторизованного пользователя')
    def test_get_orders_unauthorized_user(self):
        response = requests.get(Urls.ORDERS_URL)
        response_data = response.json()

        assert (response.status_code == 401 and response_data['success'] is False and
                response_data.get('message') == 'You should be authorised')


