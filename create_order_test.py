import allure
import requests
from faker import Faker
from data import Urls

fake = Faker()


class TestCreateOrder:

    @allure.title('Создание заказа с авторизацией')
    def test_create_order_with_authorization(self, new_user, valid_ingredient_ids, delete_user):
        _, access_token = new_user
        headers = {
            "Authorization": access_token
        }
        order_data = {
            "ingredients": valid_ingredient_ids[:3]
        }
        response = requests.post(Urls.ORDERS_URL, headers=headers, json=order_data)
        response_data = response.json()
        assert (response.status_code == 200 and response_data.get('success') is True and
                'order' in response_data and 'number' in response_data['order'])
        delete_user(access_token)

    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_authorization(self, valid_ingredient_ids):
        order_data = {
            "ingredients": valid_ingredient_ids[:3]
        }
        response = requests.post(Urls.ORDERS_URL, json=order_data)
        response_data = response.json()
        assert response.status_code == 200 and response_data.get('success') is True

    @allure.title('Создание заказа с ингредиентами')
    def test_create_order_with_ingredients(self, new_user, valid_ingredient_ids, delete_user):
        _, access_token = new_user
        headers = {
            "authorization": access_token
        }
        order_data = {
            "ingredients": valid_ingredient_ids[:3]
        }
        response = requests.post(Urls.ORDERS_URL, headers=headers, json=order_data)
        response_data = response.json()
        assert response.status_code == 200 and response_data.get('success') is True
        delete_user(access_token)

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, new_user, delete_user):
        _, access_token = new_user
        headers = {
            "Authorization": access_token
        }
        order_data = {
            "ingredients": []
        }
        response = requests.post(Urls.ORDERS_URL, headers=headers, json=order_data)
        response_data = response.json()
        assert (response.status_code == 400 and response_data.get('success') is False and
                response_data.get('message') == 'Ingredient ids must be provided')
        delete_user(access_token)

    @allure.title('Создание заказа с неверным хэшем ингредиента')
    def test_create_order_with_invalid_ingredient_hash(self, new_user, delete_user):
        _, access_token = new_user
        headers = {
            "Authorization": access_token
        }
        order_data = {
            "ingredients": ["invalid_hash"]
        }
        response = requests.post(Urls.ORDERS_URL, headers=headers, json=order_data)
        response_data = response.json()
        assert (response.status_code == 400 and response_data.get('success') is False and
                response_data.get('message') == 'One or more ids provided are incorrect')
        delete_user(access_token)

