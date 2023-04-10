import requests
import json
import time


def get_weather_data(url, headers, params):
    """
    Sends a GET request to the specified URL with the given headers and query parameters,
    and returns the JSON response data.

    Parameter
    ------------
    url: string
        The URL to send the request to.
    headers: dict
        A dictionary of headers to include in the request, including token to access the api.
    params: dict
        A dictionary of query parameters to include in the request.

    Returns
    ------------
    data: dict
        The JSON response data from the API.

    Notes
    ------------
    If the response status code is 429 (Too Many Requests) or 503 (Service Unavailable),
    the function will wait for 60 seconds before retrying the request.
    If the response status code is not 200, an error message will be printed and
    None will be returned.
    """
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
    """
    Retrieves monthly weather data for a specific state, data type, and time period.

    Parameters
    ------------
    state_info: dict
        A dictionary containing information about the state, including its FIPS code and station ID.
    data_type_id: string
        The ID of the data type to retrieve (e.g. 'TAVG' for average temperature).
    token: string
        The API token to use for authentication.
    start_date: string
        The start date of the time period to retrieve data for, in 'YYYY-MM-DD' format.
    end_date: string
        The end date of the time period to retrieve data for, in 'YYYY-MM-DD' format.

    Returns
    ------------
    state_weather_data: list
    A list of dictionaries containing the monthly weather data for the specified state,
    with each dictionary representing a single month and containing the following keys: 'date', 'value', 'station',
    'attributes'.

    Note
    ------------
    The function calls the get_weather_data() function to retrieve the data from the NOAA API.
    The date in each result is reformatted to 'YYYY-MM' format.
    """
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
    """
    Retrieves monthly weather data for multiple states and data types from the NOAA API, and saves the results to JSON
    files.

    Parameters
    ------------
    None

    Returns
    ------------
    None
    """
    token = 'GdMKePAkDaODqUBDSWbvYnpxcGPsTEfF'
    start_date = '2015-01-01'
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
            file_name = "weather_data_cache/temperature_data.json"
        elif id == 'PRCP':
            file_name = "weather_data_cache/precipitation_data.json"
        else:
            file_name = "weather_data_cache/wind_data.json"

        with open(file_name, 'w') as file:
            json.dump(id_data, file)


if __name__ == '__main__':
    main()