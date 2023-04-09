import requests
import json
import time

api_key = "jCnI1kooKyyN0nuTyus3NlQS7hyHMVgcZvm3MTrR"

area = ['East Coast', 'Midwest', 'Gulf Coast', 'Rocky Mountain', 'West Coast']
area_series = ['11', '21', '31', '41', '51']

petroleum_data = []

for i in range(len(area)):
    url = f"https://api.eia.gov/v2/petroleum/sum/snd/data/?api_key={api_key}&frequency=monthly&data[0]=value&facets[series][]=MTTUPP{area_series[i]}&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    elif response.status_code == 403:
        print(area[i])
        print('wait')
        time.sleep(60)
        response = requests.get(url)
        data = response.json()
    else:
        print('Error', response.status_code)

    state_petroleum_data = data['response']['data'][1:37]

    state_petroleum = {}
    state_petroleum['area'] = area[i]
    state_petroleum['data'] = []
    for data in state_petroleum_data:
        state_petroleum['data'].append({
            'date': data['period'],
            'value': data['value']
        })

    petroleum_data.append(state_petroleum)

with open('petroleum_data.json', 'w') as file:
    json.dump(petroleum_data, file)