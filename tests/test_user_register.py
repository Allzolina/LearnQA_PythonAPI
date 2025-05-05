from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
import pytest

@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    @allure.description("Successful user creation")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("Unsuccessful creation of user with existing email")
    def test_create_user_with_existing_email(self):
        data = self.prepare_registration_data(email='vinkotov@example.com')
        email = 'vinkotov@example.com'

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists",\
            f"Unexpected response content {response.content}"

    @allure.description("Unsuccessful creation of user with invalid email")
    def test_create_user_with_invalid_email(self):
        invalid_email = "invalidemail.com"
        data = self.prepare_registration_data(email=invalid_email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, "Invalid email format")

    @allure.description("Attempt to create user without one required parameter")
    @pytest.mark.parametrize("missing_field", ["password", "username", "firstName", "lastName", "email"])
    def test_create_user_with_missing_field(self, missing_field):
        data = self.prepare_registration_data()
        data.pop(missing_field)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, f"The following required params are missed: {missing_field}")

    @allure.description("Attempt to create user with username 1 character")
    def test_create_user_with_short_name(self):
        short_name = "a"
        data = self.prepare_registration_data(username=short_name)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, "The value of 'username' field is too short")

    @allure.description("Attempt to create user with username 250 character")
    def test_create_user_with_long_name(self):
        long_name = "a" * 251
        data = self.prepare_registration_data(username=long_name)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, "The value of 'username' field is too long")

