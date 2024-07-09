import unittest
import allure
import requests
from faker import Faker
from data import Urls

fake = Faker()


class TestUserLogin(unittest.TestCase):

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
        assert response_data['success'] is True
        cls.tokens['accessToken'] = response_data['accessToken']
        cls.tokens['refreshToken'] = response_data['refreshToken']

    @classmethod
    def tearDownClass(cls):
        headers = {
            "authorization": cls.tokens['accessToken']
        }
        response = requests.delete(Urls.USER_DELETE_URL, headers=headers)
        assert response.status_code == 202

    @allure.title('Успешная авторизация пользователя')
    def test_login_with_new_user(self):
        response = requests.post(Urls.LOGIN_URL, json=self.new_user_data)
        response_data = response.json()
        assert (response.status_code == 200 and response_data.get('success') is True and
                response_data.get('accessToken').startswith('Bearer'))

    @allure.title('Авторизация с некорректным паролем')
    def test_login_with_incorrect_password(self):
        invalid_user_data = {
            "email": fake.email(),
            "password": 'incorrect_password'
        }
        response = requests.post(Urls.LOGIN_URL, json=invalid_user_data)
        response_data = response.json()
        assert (response.status_code == 401 and response_data.get('success') is False and
                response_data.get('message') == 'email or password are incorrect')

    @allure.title('Авторизация с некорректным логином')
    def test_login_with_incorrect_login(self):
        invalid_user_data = {
            "email": 'incorrect_email',
            "password": fake.password()
        }
        response = requests.post(Urls.LOGIN_URL, json=invalid_user_data)
        response_data = response.json()
        assert (response.status_code == 401 and response_data.get('success') is False and
                response_data.get('message') == 'email or password are incorrect')
