from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        data = self.prepare_registration_data(email='vinkotov@example.com')
        email = 'vinkotov@example.com'

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists",\
            f"Unexpected response content {response.content}"
