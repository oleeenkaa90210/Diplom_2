import allure
import requests
from data import Urls


class TestGetUserOrders:
    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_user_orders(self, new_user, setup_orders, delete_user):
        _, access_token = new_user
        headers = {
            "Authorization": access_token
        }
        response = requests.get(Urls.ORDERS_URL, headers=headers)
        response_data = response.json()

        assert (response.status_code == 200 and response_data.get('success') is True and 'orders' in response_data and
                len(response_data['orders']) == 3)
        delete_user(access_token)

    @allure.title('Получение заказов неавторизованного пользователя')
    def test_get_orders_unauthorized_user(self):
        response = requests.get(Urls.ORDERS_URL)
        response_data = response.json()

        assert (response.status_code == 401 and response_data['success'] is False and
                response_data.get('message') == 'You should be authorised')
