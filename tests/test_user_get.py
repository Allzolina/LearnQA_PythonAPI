from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase
import allure


@allure.epic("Get user cases")
class TestUserGet(BaseCase):
    @allure.description("Get user info without authorization")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')

    @allure.description("Get user info authorized same user")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_auth = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response_auth, "auth_sid")
        token = self.get_header(response_auth, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response_auth, "user_id")

        response_get_auth_user = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response_get_auth_user, expected_fields)

    @allure.description("Get user info authorized another user")
    def test_get_user_details_auth_as_another_user(self):

        auth_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_auth = MyRequests.post("/user/login", data=auth_data)

        auth_sid = self.get_cookie(response_auth, "auth_sid")
        token = self.get_header(response_auth, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response_auth, "user_id")

        another_user_id = int(user_id_from_auth) + 1

        response_get_another_user = MyRequests.get(
            f"/user/{another_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        unexpected_fields = ["email", "firstName", "lastName"]

        Assertions.assert_json_has_key(response_get_another_user, "username")
        Assertions.assert_json_has_not_keys(response_get_another_user, unexpected_fields)
