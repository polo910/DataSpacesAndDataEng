import requests
response = requests.get("http://127.0.0.1:8001/observations")
data = response.json()
print("NUMBER OF OBSERVATIONS:", len(data))
print("FIRST RECORD:")
print(data[0])
