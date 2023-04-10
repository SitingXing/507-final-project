import json



class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child_name):
        child = Node(child_name)
        self.children.append(child)
        return child

    def get_child(self, val):
        if val in self.children:
            return self.children[val]
        else:
            return None


def construct_state_tree(state_info, coal_data, elec_data, gas_data, temp_data, prec_data, wind_data):
    state = Node(state_info['state'])

    energy = state.add_child('Energy')
    weather = state.add_child('Weather')

    for energy_type in ['coal', 'electricity', 'natural gas']:
        energy.add_child(energy_type)

    coal_index = -1
    for year in range(2015, 2023):
        for month in ['Q1', 'Q2', 'Q3', 'Q4']:
            month_node = energy.children[0].add_child(str(year) + '-' + month)
            month_node.add_child(coal_data['data'][coal_index]['value'])
            coal_index -= 1

    for type in ['electricity', 'natural gas']:
        if type == 'electricity':
            data = elec_data
            index = 1
        else:
            data = gas_data
            index = 2

        eg_index = -1
        for year in range(2015, 2023):
            for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
                month_node = energy.children[index].add_child(str(year) + '-' + month)
                month_node.add_child(data['data'][eg_index]['value'])
                eg_index -= 1

    for weather_type in ['temperature', 'precipitation', 'wind']:
        weather_node = weather.add_child(weather_type)

        if weather_type == 'temperature':
            weather_data = temp_data
        elif weather_type == 'precipitation':
            weather_data = prec_data
        else:
            weather_data = wind_data

        index = 0
        for year in range(2015, 2023):
            for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
                month_node = weather_node.add_child(str(year) + '-' + month)
                month_node.add_child(weather_data['data'][index]['value'])
                index += 1

    return state


def main():
    with open('state info.json', 'r') as file:
        states_info = json.load(file)[0]

    with open('energy_data_cache/coal_data.json', 'r') as file:
        coal_data = json.load(file)[0]

    with open('energy_data_cache/electricity_data.json', 'r') as file:
        electricity_data = json.load(file)[0]

    with open('energy_data_cache/natural_gas_data.json', 'r') as file:
        natural_gas_data = json.load(file)[0]

    with open('weather_data_cache/temperature_data.json', 'r') as file:
        temp_data = json.load(file)[0]

    with open('weather_data_cache/precipitation_data.json', 'r') as file:
        prec_data = json.load(file)[0]

    with open('weather_data_cache/wind_data.json', 'r') as file:
        wind_data = json.load(file)[0]

    state_test = construct_state_tree(states_info, coal_data, electricity_data, natural_gas_data, temp_data, prec_data, wind_data)



if __name__ == '__main__':
    main()