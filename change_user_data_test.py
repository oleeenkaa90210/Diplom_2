import allure
import requests
from faker import Faker
from data import Urls, UserData

fake = Faker()


class TestChangeUserData:

    @allure.title('Изменение данных пользователя с авторизацией')
    def test_update_user_with_authorization(self, new_user, delete_user):
        _, access_token = new_user
        headers = {
            "authorization": access_token
        }
        updated_user_data = {
            "email": fake.email(),
            "name": fake.name()
        }
        response = requests.patch(Urls.USER_UPDATE_URL, headers=headers, json=updated_user_data)
        response_data = response.json()
        assert response.status_code == 200 and response_data.get('success') is True
        assert response_data['user']['email'] == updated_user_data['email']
        assert response_data['user']['name'] == updated_user_data['name']
        delete_user(access_token)

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
    def test_update_user_with_existing_email(self, new_user, delete_user):
        _, access_token = new_user
        headers = {
            "authorization": access_token
        }
        updated_user_data = {
            "email": UserData.user_email,
            "name": fake.name()
        }
        response = requests.patch(Urls.USER_UPDATE_URL, headers=headers, json=updated_user_data)
        response_data = response.json()
        assert (response.status_code == 403 and response_data.get('success') is False and
                response_data.get('message') == 'User with such email already exists')
        delete_user(access_token)

