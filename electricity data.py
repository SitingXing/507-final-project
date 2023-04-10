import requests
import json
import time


def get_electricity_data(api_key, state_info_data):
    """
    Retrieves monthly electricity consumption data for each state in the provided state information data using the EIA API,
    and returns the results as a list of dictionaries.

    Parameters
    ------------
    api_key: string
        The API key for authentication with the EIA API.
    state_info_data: list
        A list of dictionaries containing state information data, including state
        abbreviations and names.

    Returns
    ------------
    electricity_data: list
        A list of dictionaries containing coal consumption data for each state, with keys
        'state' and 'data'. The 'data' key maps to a list of dictionaries containing consumption data for each month, with
        keys 'date', 'location', 'location_detail', 'value', and 'units'.
    """
    electricity_data = []

    for state in state_info_data:
        url = f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?api_key={api_key}&frequency=monthly&data[0]=generation&facets[fueltypeid][]=ALL&facets[location][]={state['abbr']}&facets[sectorid][]=1&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

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

        state_electricity_data = data['response']['data'][1:97]

        state_electricity = {}
        state_electricity['state'] = state['state']
        state_electricity['data'] = []
        for data in state_electricity_data:
            state_electricity['data'].append({
                'date': data['period'],
                'location': data['location'],
                'location_detail': data['stateDescription'],
                'value': data['generation'],
                'units': data['generation-units']
            })

        electricity_data.append(state_electricity)

    return electricity_data


def main():
    """
    Fetches data on electricity consumption and quality for each state using the EIA API and stores the data in a JSON file.

    Parameters
    ------------
    None

    Returns
    ------------
    None
    """
    api_key = "jCnI1kooKyyN0nuTyus3NlQS7hyHMVgcZvm3MTrR"

    with open('state info.json', 'r') as file:
        data = json.load(file)

    electricity_data = get_electricity_data(api_key, data)

    with open('energy_data_cache/electricity_data.json', 'w') as file:
        json.dump(electricity_data, file)


if __name__ == '__main__':
    main()