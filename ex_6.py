import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
count_redirect = len(response.history)
end_url = response.url
print(end_url)
print(count_redirect)
