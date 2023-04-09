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


def construct_state_tree(state_info, coal_data, elec_data, gas_data, weather_data):
    state = Node(state_info['state'])

    energy = state.add_child('Energy')
    weather = state.add_child('Weather')

    for energy_type in ['coal', 'electricity', 'natural gas']:
        energy.add_child(energy_type)

    coal_index = -1
    for year in range(2020, 2023):
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
        for year in range(2020, 2023):
            for month in ['01', '02', '03', '05', '06', '07', '08', '09', '10', '11', '12']:
                month_node = energy.children[index].add_child(str(year) + '-' + month)
                month_node.add_child(data['data'][eg_index]['value'])
                eg_index -= 1

    for weather_type in ['temperature', 'precipitation', 'wind']:
        weather_node = weather.add_child(weather_type)

        if weather_type == 'temperature':
            type_id = 'TAVG'
        elif weather_type == 'precipitation':
            type_id = 'PRCP'
        else:
            type_id = 'AWND'

        index = 0
        for year in range(2020, 2023):
            for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
                month_node = weather_node.add_child(str(year) + '-' + month)
                month_node.add_child(weather_data[type_id][index]['value'])
                index += 1

    return state


def construct_area_tree(area_name, state_tree, petro_data):
    area = Node(area_name)

    area.children.append(state_tree)

    area.add_child('petroleum')

    petro_index = -1
    for year in range(2020, 2023):
        for month in ['01', '02', '03', '05', '06', '07', '08', '09', '10', '11', '12']:
            month_node = energy.children[0].add_child(str(year) + '-' + month)
            month_node.add_child(coal_data['data'][coal_index]['value'])
            coal_index -= 1


# def construct_area_tree(area_name, state_tree, petro_data):
#     area_node = Node(area_name)
#     area_node.add_child(stat)
    

    

# with open('state info.json', 'r') as file:
#     states_info = json.load(file)

# with open('electricity_data.json', 'r') as file:
#     elec_data = json.load(file)

# with open('coal_data.json', 'r') as file:
#     coal_data = json.load(file)

# with open('natural_gas_data.json', 'r') as file:
#     gas_data = json.load(file)

# with open('weather_data/Alabama.json', 'r') as file:
#     weather_data = json.load(file)

# tree_test = construct_state_tree(states_info[0], coal_data[0], elec_data[0], gas_data[0], weather_data)
# print(len(tree_test.children[1].children[0].children))

#area_list = ['East Coast', 'Midwest', 'Gulf Coast', 'Rocky Mountain', 'West Coast']