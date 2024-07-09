import unittest
import allure
import requests
from faker import Faker
from data import Urls

fake = Faker()


class TestChangeUserData(unittest.TestCase):
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

    @classmethod
    def tearDownClass(cls):
        headers = {
            "authorization": cls.tokens['accessToken']
        }
        response = requests.delete(Urls.USER_DELETE_URL, headers=headers)
        assert response.status_code == 202

    @allure.title('Изменение данных пользователя с авторизацией')
    def test_update_user_with_authorization(self):
        headers = {
            "authorization": self.tokens['accessToken']
        }
        updated_user_data = {
            "email": fake.email(),
            "name": fake.name()
        }
        response = requests.patch(Urls.USER_UPDATE_URL, headers=headers, json=updated_user_data)
        response_data = response.json()
        assert (response.status_code == 200 and response_data.get('success') is True and
                response_data['user']['email'] == updated_user_data['email'] and
                response_data['user']['name'] == updated_user_data['name'])

    @allure.title('Изменение данных пользователя без авторизации')
    def test_update_user_without_authorization(self):
        updated_user_data = {
            "email": fake.email(),
            "name": fake.name()
        }
        response = requests.patch(Urls.USER_UPDATE_URL, json=updated_user_data)
        response_data = response.json()
        assert (response.status_code == 401 and response_data.get('success') is False and
                response_data.get('message') == 'You should be authorised')

    @allure.title('Изменение данных на почту, которая уже используется')
    def test_update_user_with_existing_email(self):
        headers = {
            "authorization": self.tokens['accessToken']
        }
        existing_user_email = 'zxcvbnm@ya.ru'
        updated_user_data = {
            "email": existing_user_email,
            "name": fake.name()
        }
        response = requests.patch(Urls.USER_UPDATE_URL, headers=headers, json=updated_user_data)
        response_data = response.json()
        assert (response.status_code == 403 and response_data.get('success') is False and
                response_data.get('message') == 'User with such email already exists')
