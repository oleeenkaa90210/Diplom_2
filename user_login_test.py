import allure
import requests
from faker import Faker
from data import Urls

fake = Faker()


class TestUserLogin:

    @allure.title('Успешная авторизация пользователя')
    def test_login_with_new_user(self, new_user, delete_user):
        new_user_data, access_token = new_user
        headers = {
            "Authorization": access_token
        }
        response = requests.post(Urls.LOGIN_URL, headers=headers, json=new_user_data)
        response_data = response.json()
        assert (response.status_code == 200 and response_data.get('success') is True and
                response_data.get('accessToken').startswith('Bearer'))
        delete_user(access_token)

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
