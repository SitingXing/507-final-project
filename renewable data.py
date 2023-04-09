import requests
import json
import time

api_key = "jCnI1kooKyyN0nuTyus3NlQS7hyHMVgcZvm3MTrR"

renewable_data = []

url = f"https://api.eia.gov/v2/total-energy/data/?api_key={api_key}&frequency=monthly&data[0]=value&facets[msn][]=RETCBUS&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
elif response.status_code == 403:
    print('wait')
    time.sleep(60)
    response = requests.get(url)
    data = response.json()
else:
    print('Error', response.status_code)

renewable_data = data['response']['data'][0:36]

renewable = []
for data in renewable_data:
    renewable.append({
        'date': data['period'],
        'value': data['value']
    })

with open('renewable_data.json', 'w') as file:
    json.dump(renewable, file)