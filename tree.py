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
            try:
                if month_node.name == coal_data['data'][coal_index]['time']:
                    month_node.add_child(coal_data['data'][coal_index]['value'])
                    coal_index -= 1
            except IndexError:
                break

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
                try:
                    if month_node.name == data['data'][index]['date']:
                        month_node.add_child(data['data'][eg_index]['value'])
                        eg_index -= 1
                except IndexError:
                    break

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
                try:
                    if month_node.name == weather_data['data'][index]['date']:
                        month_node.add_child(weather_data['data'][index]['value'])
                        index += 1
                except IndexError:
                    break

    return state


def get_data_from_cache(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    return data


def main():
    states_info = get_data_from_cache('state info.json')
    coal_data = get_data_from_cache('energy_data_cache/coal_data.json')
    electricity_data = get_data_from_cache('energy_data_cache/electricity_data.json')
    natural_gas_data = get_data_from_cache('energy_data_cache/natural_gas_data.json')
    temperature_data = get_data_from_cache('weather_data_cache/temperature_data.json')
    precipitation_data = get_data_from_cache('weather_data_cache/precipitation_data.json')
    wind_data = get_data_from_cache('weather_data_cache/wind_data.json')

    root = Node('USA')

    for i in range(50):
        state_tree = construct_state_tree(states_info[i], coal_data[i], electricity_data[i], natural_gas_data[i], temperature_data[i], precipitation_data[i], wind_data[i])
        root.children.append(state_tree)


if __name__ == '__main__':
    main()