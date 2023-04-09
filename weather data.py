import requests
import json
import time

base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?'
headers = {"token": 'GdMKePAkDaODqUBDSWbvYnpxcGPsTEfF'}
dataset_id = 'GSOM'
start_date = '2020-01-01'
end_date = '2022-12-31'
limit = 1000

data_type_ids = ['TAVG', 'PRCP', 'AWND']
months = ['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10', '2021-11', '2021-12', '2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06', '2022-07', '2022-08', '2022-09', '2022-10', '2022-11', '2022-12']


def get_weather_data(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
    elif response.status_code == 429 or 503:
        print('wait')
        time.sleep(60)
        response = requests.get(base_url, headers=headers, params=params)
        data = response.json()
    else:
        print('Error', response.status_code)
    return data


def get_state_monthly_weather(state_info, data_type_id):
    state_weather_data = []
    params = {
        'datasetid': dataset_id,
        'datatypeid': data_type_id,
        'locationid': f"FIPS:{state_info['fips_code']}",
        'stationid': state_info['station_id'],
        'startdate': start_date,
        'enddate': end_date,
        'limit': limit,
        'units': 'metric',
    }

    data = get_weather_data(base_url, headers=headers, params=params)

    for result in data['results']:
        item = {}
        item['date'] = result['date']
        item['value'] = result['value']
        state_weather_data.append(item)

    return state_weather_data


#Write data into files
with open('state info.json', 'r') as file:
    data = json.load(file)

weather_data_files = []
for state in data:
    json_filename = f"{state['state']}.json"

    state_weather = []

    for id in data_type_ids:
        state_weather.append(id)
        state_weather_data = get_state_monthly_weather(state, id)
        state_weather.append(state_weather_data)

    with open(f'weather_data/{json_filename}', 'w') as file:
        json.dump(state_weather, file)

    weather_data_files.append(json_filename)

    print(json_filename)

with open('weather_data_files.json', 'w') as file:
    json.dump(weather_data_files, file)