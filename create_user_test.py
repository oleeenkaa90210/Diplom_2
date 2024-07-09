import allure
import unittest
import requests
from faker import Faker
from data import Urls

fake = Faker('ru_RU')


def generate_random_user_data():
    user_data = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    return user_data


@classmethod
def tearDownClass(cls):
    headers = {
        "authorization": cls.tokens['accessToken']
    }
    response = requests.delete(Urls.USER_DELETE_URL, headers=headers)
    assert response.status_code == 202


class TestUserCreation(unittest.TestCase):

    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self):
        valid_user_data = generate_random_user_data()
        response = requests.post(Urls.REGISTER_URL, json=valid_user_data)
        response_data = response.json()
        assert response.status_code == 200 and response_data.get('success') is True

    @allure.title('Создание уже зарегистрированного пользователя')
    def test_register_existing_user(self):
        valid_user_data = generate_random_user_data()
        response = requests.post(Urls.REGISTER_URL, json=valid_user_data)
        response_data = response.json()
        assert response.status_code == 200 and response_data.get('success') is True

        duplicate_response = requests.post(Urls.REGISTER_URL, json=valid_user_data)
        duplicate_response_data = duplicate_response.json()
        assert (duplicate_response.status_code == 403 and duplicate_response_data.get('success') is False and
                duplicate_response.json().get('message') == "User already exists")

    @allure.title('Создание пользователя без пароля')
    def test_create_user_without_password(self):
        valid_user_data = generate_random_user_data()
        user_data_without_password = valid_user_data.copy()
        user_data_without_password.pop('password', None)

        response = requests.post(Urls.REGISTER_URL, json=user_data_without_password)
        response_data = response.json()
        assert (response.status_code == 403 and response_data.get('success') is False and
                response.json().get('message') == 'Email, password and name are required fields')
