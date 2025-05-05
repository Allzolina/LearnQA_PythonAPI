from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
import allure


@allure.epic("Edit user info cases")
class TestUserEdit(BaseCase):
    @allure.description("Successful edit user info")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_register, 200)
        Assertions.assert_json_has_key(response_register, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response_register, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # EDIT
        new_name = "Change name"

        response_edit = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response_edit, 200)

        # GET
        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response_get,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.description("Attempt to edit user data without being authorized")
    def test_edit_user_not_auth(self):
        with allure.step("Register a new user"):
            register_data = self.prepare_registration_data()
            response_register = MyRequests.post("/user/", data=register_data)
            Assertions.assert_code_status(response_register, 200)
            user_id = self.get_json_value(response_register, "id")

        with allure.step("Try to edit user data without auth"):
            response_edit = MyRequests.put(
                f"/user/{user_id}",
                data={"firstName": "New Name"}
            )
            Assertions.assert_code_status(response_edit, 400)
            Assertions.assert_json_value_by_name(response_edit, "error", "Auth token not supplied",
                                                 "Incorrect error message")

    @allure.description("Attempt to edit user data while being authorized as another user")
    def test_edit_user_as_another_user(self):
        with allure.step("Register user 1"):
            user1_data = self.prepare_registration_data()
            response_user1 = MyRequests.post("/user/", data=user1_data)
            Assertions.assert_code_status(response_user1, 200)
            user1_id = self.get_json_value(response_user1, "id")

        with allure.step("Register user 2"):
            user2_data = self.prepare_registration_data()
            response_user2 = MyRequests.post("/user/", data=user2_data)
            Assertions.assert_code_status(response_user2, 200)

        with allure.step("Login as user 2"):
            login_data = {
                'email': user2_data['email'],
                'password': user2_data['password']
            }
            response_login = MyRequests.post("/user/login", data=login_data)
            Assertions.assert_code_status(response_login, 200)
            auth_sid = self.get_cookie(response_login, "auth_sid")
            token = self.get_header(response_login, "x-csrf-token")

        with allure.step("Attempt to edit user 1 data as user 2"):
            response_edit = MyRequests.put(
                f"/user/{user1_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": "Hacked Name"}
            )
            Assertions.assert_code_status(response_edit, 400)
            Assertions.assert_json_value_by_name(
                response_edit,
                "error",
                "This user can only edit their own data.",
                "Incorrect error message")

    @allure.description("Attempt to edit user email to an invalid value without @")
    def test_edit_user_email_to_invalid(self):
        with allure.step("Register a new user"):
            register_data = self.prepare_registration_data()
            response_register = MyRequests.post("/user/", data=register_data)
            Assertions.assert_code_status(response_register, 200)
            user_id = self.get_json_value(response_register, "id")

        with allure.step("Login as the registered user"):
            login_data = {
                'email': register_data['email'],
                'password': register_data['password']
            }
            response_login = MyRequests.post("/user/login", data=login_data)
            Assertions.assert_code_status(response_login, 200)
            auth_sid = self.get_cookie(response_login, "auth_sid")
            token = self.get_header(response_login, "x-csrf-token")

        with allure.step("Attempt to edit email to an invalid format"):
            new_email = "invalidemail.com"
            response_edit = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"email": new_email}
            )
            Assertions.assert_code_status(response_edit, 400)
            Assertions.assert_json_value_by_name(response_edit, "error", "Invalid email format",
                                                 "Incorrect error message")

    @allure.description("Attempt to edit  firstName to a very short value (1 character)")
    def test_edit_user_first_name_to_short(self):
        with allure.step("Register a new user"):
            register_data = self.prepare_registration_data()
            response_register = MyRequests.post("/user/", data=register_data)
            Assertions.assert_code_status(response_register, 200)
            user_id = self.get_json_value(response_register, "id")

        with allure.step("Login as the registered user"):
            login_data = {
                'email': register_data['email'],
                'password': register_data['password']
            }
            response_login = MyRequests.post("/user/login", data=login_data)
            Assertions.assert_code_status(response_login, 200)
            auth_sid = self.get_cookie(response_login, "auth_sid")
            token = self.get_header(response_login, "x-csrf-token")

        with allure.step("Attempt to change firstName to a short value"):
            response_edit = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": "A"}
            )
            Assertions.assert_code_status(response_edit, 400)
            Assertions.assert_json_value_by_name(response_edit, "error", "The value for field `firstName` is too short",
                                                 "Incorrect error message")
