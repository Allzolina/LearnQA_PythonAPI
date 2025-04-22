import requests


class TestCookie:
    def test_check_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        cookies = response.cookies
        expected_name_cookie = "HomeWork"
        expected_value_cookie = "hw_value"

        assert expected_name_cookie in cookies, f" There is no cookie named {expected_name_cookie}"
        value_cookie = cookies[expected_name_cookie]
        assert value_cookie == expected_value_cookie, f" The cookie value does not match.\n Expected: {expected_value_cookie} \n Actual: {value_cookie}"
