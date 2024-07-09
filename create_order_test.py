import unittest
import allure
import requests
from faker import Faker
from data import Urls

fake = Faker()


class TestCreateOrder(unittest.TestCase):
    valid_ingredient_ids = []
    tokens = {
        "accessToken": "",
        "refreshToken": ""
    }

    @classmethod
    def setUpClass(cls):
        response = requests.get(Urls.INGREDIENTS_URL)
        ingredients = response.json()
        cls.valid_ingredient_ids = [ingredient['_id'] for ingredient in ingredients['data'] if ingredient['_id']]
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

    @classmethod
    def tearDownClass(cls):
        headers = {
            "authorization": cls.tokens['accessToken']
        }
        response = requests.delete(Urls.USER_DELETE_URL, headers=headers)
        assert response.status_code == 202

    @allure.title('Создание заказа с авторизацией')
    def test_create_order_with_authorization(self):
        headers = {
            "authorization": self.tokens['accessToken']
        }
        order_data = {
            "ingredients": self.valid_ingredient_ids[:3]
        }
        response = requests.post(Urls.ORDERS_URL, headers=headers, json=order_data)
        response_data = response.json()
        assert (response.status_code == 200 and response_data.get('success') is True and
                'order' in response_data and 'number' in response_data['order'])

    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_authorization(self):
        order_data = {
            "ingredients": self.valid_ingredient_ids[:3]
        }
        response = requests.post(Urls.ORDERS_URL, json=order_data)
        response_data = response.json()
        assert response.status_code == 200 and response_data.get('success') is True

    @allure.title('Создание заказа с ингредиентами')
    def test_create_order_with_ingredients(self):
        headers = {
            "authorization": self.tokens['accessToken']
        }
        order_data = {
            "ingredients": self.valid_ingredient_ids[:3]
        }
        response = requests.post(Urls.ORDERS_URL, headers=headers, json=order_data)
        response_data = response.json()
        assert response.status_code == 200 and response_data.get('success') is True

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self):
        headers = {
            "authorization": self.tokens['accessToken']
        }
        order_data = {
            "ingredients": []
        }
        response = requests.post(Urls.ORDERS_URL, headers=headers, json=order_data)
        response_data = response.json()
        assert (response.status_code == 400 and response_data.get('success') is False and
                response_data.get('message') == 'Ingredient ids must be provided')

    @allure.title('Создание заказа с неверным хэшем ингредиента')
    def test_create_order_with_invalid_ingredient_hash(self):
        headers = {
            "authorization": self.tokens['accessToken']
        }
        order_data = {
            "ingredients": ["invalid_hash"]
        }
        response = requests.post(Urls.ORDERS_URL, headers=headers, json=order_data)
        response_data = response.json()
        assert (response.status_code == 400 and response_data.get('success') is False and
                response_data.get('message') == 'One or more ids provided are incorrect')
