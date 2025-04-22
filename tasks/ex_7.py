import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
response_to_question = requests.get(url)
print(f" Ответ на вопрос 1 : {response_to_question.text}")


response_to_question2 = requests.options(url, params={"method": "OPTIONS"})
print(f" Ответ на вопрос 2 : {response_to_question2.text}")

response_to_question3 = requests.get(url, params={"method": "GET"})
print(f" Ответ на вопрос 3 : {response_to_question3.text}")

methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
supported_methods = ['GET', 'POST', 'PUT', 'DELETE']


for request_method in methods:
    for param_method in methods:
        if request_method == 'GET':
            response = requests.get(url, params={'method': param_method})
        elif request_method == 'POST':
            response = requests.post(url, data={'method': param_method})
        elif request_method == 'PUT':
            response = requests.put(url, data={'method': param_method})
        elif request_method == 'DELETE':
            response = requests.delete(url, data={'method': param_method})
        elif request_method == 'HEAD':
            response = requests.head(url, data={'method': param_method})
        elif request_method == 'OPTIONS':
            response = requests.options(url, data={'method': param_method})
        elif request_method == 'PATCH':
            response = requests.patch(url, data={'method': param_method})

        if request_method not in supported_methods:
            expected = 'Wrong HTTP method'
            actual = response.text
            if actual != expected:
                print(f"[НЕСОВПАДЕНИЕ] Метод запроса: {request_method}, параметр: {param_method}")
                print(f"   Ожидаемый результат: '{expected}', Фактический результат: '{actual}'\n")

        else:
            if request_method == param_method:
                expected = {"success": "!"}
                actual = response.json()
            else:
                expected = 'Wrong method provided'
                actual = response.text

            if actual != expected:
                print(f"   [НЕСОВПАДЕНИЕ] Метод запроса: {request_method}, параметр: {param_method}")
                print(f"   Ожидаемый результат: {expected}, Фактический результат: {actual}\n")
