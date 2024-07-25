import allure
import requests
from faker import Faker
from data import Urls

fake = Faker()


class TestUserCreation:

    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self, new_user_data):
        valid_user_data = new_user_data
        response = requests.post(Urls.REGISTER_URL, json=valid_user_data)
        response_data = response.json()
        assert response.status_code == 200 and response_data.get('success') is True

    @allure.title('Создание уже зарегистрированного пользователя')
    def test_register_existing_user(self, new_user_data):
        response = requests.post(Urls.REGISTER_URL, json=new_user_data)
        response_data = response.json()
        assert response.status_code == 200 and response_data.get('success') is True, "User registration failed"

        duplicate_response = requests.post(Urls.REGISTER_URL, json=new_user_data)
        duplicate_response_data = duplicate_response.json()
        assert (duplicate_response.status_code == 403 and duplicate_response_data.get('success') is False and
                duplicate_response.json().get('message') == "User already exists")

    @allure.title('Создание пользователя без пароля')
    def test_create_user_without_password(self, new_user_data):
        user_data_without_password = new_user_data.copy()
        user_data_without_password.pop('password', None)

        response = requests.post(Urls.REGISTER_URL, json=user_data_without_password)
        response_data = response.json()
        assert (response.status_code == 403 and response_data.get('success') is False and
                response.json().get('message') == 'Email, password and name are required fields')
