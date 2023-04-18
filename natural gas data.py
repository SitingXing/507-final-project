import requests
import json
import time


def get_natural_gas_data(api_key, state_info_data):
    """
    Retrieves monthly natural gas consumption data for each state in the provided state information data using the EIA API,
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
    natural_gas_data: list
        A list of dictionaries containing coal consumption data for each state, with keys
        'state' and 'data'. The 'data' key maps to a list of dictionaries containing consumption data for each month, with
        keys 'date', 'location', 'data_description', 'value', and 'unit'.
    """
    natural_gas_data = []

    for state in state_info_data:
        if state['natural_gas_series'] != '':
            url = f"https://api.eia.gov/v2/natural-gas/sum/snd/data/?api_key={api_key}&frequency=monthly&data[0]=value&facets[series][]={state['natural_gas_series']}&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

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

            state_natural_gas_data = data['response']['data'][1:97]

            state_gas = {}
            state_gas['state'] = state['state']
            state_gas['data'] = []
            for data in state_natural_gas_data:
                state_gas['data'].append({
                    'date': data['period'],
                    'location': data['area-name'],
                    'data_description': data['series-description'],
                    'value': data['value'],
                    'unit': data['units']
                })

        else:
            state_gas = {}
            state_gas['state'] = state['state']
            state_gas['data'] = []

        natural_gas_data.append(state_gas)

    return natural_gas_data


def main():
    """
    Fetches data on natural gas consumption and quality for each state using the EIA API and stores the data in a JSON file.

    Parameters
    ------------
    None

    Returns
    ------------
    None
    """
    with open('API_key.txt', 'r') as file:
        key_data = file.readlines()

    api_key = key_data[0].split(':')[1].strip()

    with open('state info.json', 'r') as file:
        data = json.load(file)

    natural_gas_data = get_natural_gas_data(api_key, data)

    with open('energy_data_cache/natural_gas_data.json', 'w') as file:
        json.dump(natural_gas_data, file)


if __name__ == '__main__':
    main()