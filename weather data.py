import requests
import json
import time


def get_weather_data(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
    elif response.status_code == 429 or 503:
        print('wait')
        time.sleep(60)
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
    else:
        print('Error', response.status_code)
    return data


def get_state_monthly_weather(state_info, data_type_id, token, start_date, end_date):
    base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?'
    headers = {"token": token}

    state_weather_data = []
    params = {
        'datasetid': 'GSOM',
        'datatypeid': data_type_id,
        'locationid': f"FIPS:{state_info['fips_code']}",
        'stationid': state_info['station_id'],
        'startdate': start_date,
        'enddate': end_date,
        'limit': 1000,
        'units': 'metric',
    }

    data = get_weather_data(base_url, headers=headers, params=params)

    for result in data['results']:
        result['date'] = result['date'].split('-')[0] + '-' + result['date'].split('-')[1]
        state_weather_data.append(result)

    return state_weather_data


def main():
    token = 'GdMKePAkDaODqUBDSWbvYnpxcGPsTEfF'
    start_date = '2018-01-01'
    end_date = '2022-12-31'

    data_type_ids = ['TAVG', 'PRCP', 'AWND']

    with open('state info.json', 'r') as file:
        data = json.load(file)

    for id in data_type_ids:
        id_data = []
        for state in data:
            state_weather = {}
            state_weather_data = get_state_monthly_weather(state, id, token, start_date, end_date)
            state_weather['state'] = state['state']
            state_weather['data'] = state_weather_data
            id_data.append(state_weather)

        if id == 'TAVG':
            file_name = "temperature_data.json"
        elif id == 'PRCP':
            file_name = "precipitation_data.json"
        else:
            file_name = "wind_data.json"

        with open(file_name, 'w') as file:
            json.dump(id_data, file)


if __name__ == '__main__':
    main()