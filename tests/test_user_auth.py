import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookie",
        "no_token"
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response_login, "auth_sid")
        self.token = self.get_header(response_login, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response_login, "user_id")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("This test successfully authorize user by email and password")
    def test_auth_user(self):
        response_auth = MyRequests.get(
            "/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response_auth,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @allure.description("This test check authorization status w/o sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        url = "/user/auth"
        if condition == "no_cookie":
            response_auth = MyRequests.get(
                url, headers={"x-csrf-token": self.token}
            )
        else:
            response_auth = MyRequests.get(
                url, cookies={"auth_sid": self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response_auth,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
