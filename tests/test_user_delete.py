from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase
import allure


@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):
    @allure.description("Attempt to delete user with ID 2")
    def test_delete_user_with_id_2(self):
        with allure.step("Authorized  user with ID 2"):
            auth_data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }

            response_auth = MyRequests.post("/user/login", data=auth_data)

            Assertions.assert_code_status(response_auth, 200)
            auth_sid = self.get_cookie(response_auth, "auth_sid")
            token = self.get_header(response_auth, "x-csrf-token")
            user_id = self.get_json_value(response_auth, "user_id")

        with allure.step("Delete user with ID 2"):
            response_delete = MyRequests.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response_delete,
                "error",
                "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
                "Incorrect error message"
            )

    @allure.description("Successfully deleted user")
    def test_successfully_deleted_user(self):
        with allure.step("Register a new user"):
            register_data = self.prepare_registration_data()
            response_create = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response_create, 200)
            user_id = self.get_json_value(response_create, "id")

        with allure.step("Authorize the new user"):
            login_data = {
                'email': register_data['email'],
                'password': register_data['password']
            }

            response_auth = MyRequests.post("/user/login", data=login_data)

            Assertions.assert_code_status(response_auth, 200)
            auth_sid = self.get_cookie(response_auth, "auth_sid")
            token = self.get_header(response_auth, "x-csrf-token")

        with allure.step("Delete the user"):
            response_delete = MyRequests.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_code_status(response_delete, 200)

        with allure.step("Try to get deleted user data by ID"):
            response_get = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_code_status(response_get, 404)
            Assertions.assert_response_text(
                response_get,
                "User not found"
            )

    @allure.description("Attempt to delete another user by an authorized user")
    def test_delete_another_user_(self):
        with allure.step("Register user 1"):
            register_data_user_1 = self.prepare_registration_data()
            response_create_user_1 = MyRequests.post("/user/", data=register_data_user_1)

            Assertions.assert_code_status(response_create_user_1, 200)

        with allure.step("Register user 2"):
            register_data_user_2 = self.prepare_registration_data()
            response_create_user_2 = MyRequests.post("/user/", data=register_data_user_2)

            Assertions.assert_code_status(response_create_user_2, 200)
            user_2_id = self.get_json_value(response_create_user_2, "id")

        with allure.step("Authorize user 1"):
            login_data = {
                'email': register_data_user_1['email'],
                'password': register_data_user_1['password']
            }

            response_auth = MyRequests.post("/user/login", data=login_data)

            Assertions.assert_code_status(response_auth, 200)
            auth_sid = self.get_cookie(response_auth, "auth_sid")
            token = self.get_header(response_auth, "x-csrf-token")

        with allure.step("Delete the user 2 "):
            response_delete = MyRequests.delete(
                f"/user/{user_2_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_code_status(response_delete, 200)

        with allure.step("Checking that the user 2 is not deleted"):
            response_get = MyRequests.get(
                f"/user/{user_2_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_code_status(response_get, 200)
            Assertions.assert_json_has_key(response_get, "username")
