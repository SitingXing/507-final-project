import requests
import json
import time

api_key = "jCnI1kooKyyN0nuTyus3NlQS7hyHMVgcZvm3MTrR"

with open('state info.json', 'r') as file:
    data = json.load(file)

coal_data = []

for state in data:
    url = f"https://api.eia.gov/v2/coal/consumption-and-quality/data/?api_key={api_key}&frequency=quarterly&data[0]=consumption&facets[location][]={state['abbr']}&facets[sector][]=98&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    elif response.status_code == 403:
        print(state['state'])
        print('wait')
        time.sleep(60)
        response = requests.get(url)
        data = response.json()
    else:
        print('Error', response.status_code)

    state_coal_data = data['response']['data'][0:12]

    state_coal = {}
    state_coal['state'] = state['state']
    state_coal['data'] = []
    for data in state_coal_data:
        state_coal['data'].append({
            'date': data['period'],
            'value': data['consumption']
        })

    coal_data.append(state_coal)

with open('coal_data.json', 'w') as file:
    json.dump(coal_data, file)