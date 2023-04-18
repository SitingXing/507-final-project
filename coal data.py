import requests
import json
import time


def get_coal_data(api_key, state_info_data):
    """
    Retrieves quarterly coal consumption data for each state in the provided state information data using the EIA API,
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
    coal_data: list
        A list of dictionaries containing coal consumption data for each state, with keys
        'state' and 'data'. The 'data' key maps to a list of dictionaries containing consumption data for each quarter, with
        keys 'time', 'location', 'location_detail', 'value', and 'units'.
    """
    coal_data = []

    for state in state_info_data:
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

        state_coal_data = data['response']['data'][0:32]

        state_coal = {}
        state_coal['state'] = state['state']
        state_coal['data'] = []
        for data in state_coal_data:
            state_coal['data'].append({
                'time': data['period'],
                'location': data['location'],
                'location_detail': data['stateDescription'],
                'value': data['consumption'],
                'units': data['consumption-units']
            })

        coal_data.append(state_coal)

    return coal_data


def main():
    """
    Fetches data on coal consumption and quality for each state using the EIA API and stores the data in a JSON file.

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

    coal_data = get_coal_data(api_key, data)

    with open('energy_data_cache/coal_data.json', 'w') as file:
        json.dump(coal_data, file)


if __name__ == '__main__':
    main()