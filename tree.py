import json



class Node:
    def __init__(self, val):
        self.value = val
        self.children = {}

    def add_child(self, child_val):
        child = Node(child_val)
        self.children[child_val] = child
        return child

    def get_child(self, val):
        if val in self.children:
            return self.children[val]
        else:
            return None


def construct_state_tree(state_info, coal_data, elec_gas_data, weather_data):
    state = Node(state_info['state'])

    energy = state.add_child('Energy')
    weather = state.add_child('Weather')

    for energy_type in ['coal', 'electricity', 'natural gas', 'petroleum', 'renewable']:
        energy.add_child(energy_type)

    coal_index = -1
    for year in range(2020, 2023):
        for month in ['Q1', 'Q2', 'Q3', 'Q4']:
            month_node = energy.children['coal'].add_child(str(year) + '-' + month)
            month_node.add_children(coal_data['data'][coal_index]['value'])
            coal_index -= 1

    for type in ['electricity', 'natural gas']:
        eg_index = -1
        for year in range(2020, 2023):
            for month in ['01', '02', '03', '05', '06', '07', '08', '09', '10', '11', '12']:
                month_node = energy.children[type].add_child(str(year) + '-' + month)
                month_node.add_children(elec_gas_data['data'][eg_index]['value'])
                eg_index -= 1

    for weather_type in ['temperature', 'precipitation', 'wind']:
        weather.add_child(weather_type)

        index = 0
        for year in range(2020, 2023):
            for month in ['01', '02', '03', '05', '06', '07', '08', '09', '10', '11', '12']:
                month_node = weather.children[weather_type].add_child(str(year) + '-' + month)
                month_node.add_children(weather_data['TAVG'][index]['value'])
                index += 1

    


    # for weather_type in ['temperature', 'precipitation', 'wind']:
    #     weather_node = weather.add_child(weather_type)

    #     for year in range(2020, 2023):
    #         for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
    #             month_node = weather_node.add_child(str(year) + '-' + month)
    #             month_node.add_child('Value')



# with open('state info.json', 'r') as file:
#     states_info = json.load(file)

# with open('electricity_data.json', 'r') as file:
#     elec_data = json.load(file)

# print(elec_data)

# root = Node('USA')

# for state_info in states_info:
#     state_tree = construct_state_tree(state_info)
#     root.add_child(state_tree)