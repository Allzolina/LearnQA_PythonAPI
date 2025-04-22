import requests


class TestHeaders:
    def test_check_headers(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        headers = response.headers
        expected_name_header = "x-secret-homework-header"
        expected_value_header = "Some secret value"

        assert expected_name_header in headers, f" There is no header named {expected_name_header}"
        value_header = headers[expected_name_header]
        assert value_header == expected_value_header, f" The header value does not match.\n Expected: {expected_value_header} \n Actual: {value_header}"
