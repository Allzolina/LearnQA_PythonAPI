import requests
import time


url = "https://playground.learnqa.ru/ajax/api/longtime_job"

response_create_task = requests.get(url)
data = response_create_task.json()
seconds = data["seconds"]
token = data["token"]

params = {"token": token}
response_check_status = requests.get(url, params=params)
data = response_check_status.json()
status = data["status"]
assert status == "Job is NOT ready"

time.sleep(seconds)

response_check_result = requests.get(url, params=params)
data = response_check_result.json()
status = data["status"]
assert status == "Job is ready"
assert 'result' in data
