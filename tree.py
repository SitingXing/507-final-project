import json


class Node:
    """
    A class representing a node in a tree.

    Instance Attributes
    -------------------
    name: string
        The name of the node.
    children: list
        A list of the node's children.
    """
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child_name):
        """
        Adds a child node with the given name to the current node.
        Returns the newly created child node.

        Parameters
        ------------
        child_name: string
            The name of the child node to be created.

        Returns
        ------------
        Node: Node object
            The newly created child node.
        """
        child = Node(child_name)
        self.children.append(child)
        return child

    def get_child(self, val):
        """
        Returns the child node with the given name.
        If the child does not exist, returns None.

        Parameters
        ------------
        val: string
            The name of the child node to retrieve.

        Returns
        ------------
        Node or None:
            The child node with the given name, or None if it does not exist.
        """
        if val in self.children:
            return self.children[val]
        else:
            return None

    def to_dict(self):
        """Recursively convert the node and its children into a dictionary.

        Returns
        ------------
        dict:
            A dictionary representation of the node and its children.
            The dictionary has two keys:
            - 'data': The name of the node.
            - 'children': A list of dictionaries, each representing a child node.
        """
        d = {'data': self.name}
        if self.children:
            d['children'] = [child.to_dict() for child in self.children]
        return d


def print_tree(node, level=0):
    """
    Prints the tree structure with indentation to show the hierarchical relationship between the nodes.

    Parameters
    ------------
    node: object
        the Node object to start printing from
    level: int
        the current level of indentation

    Returns
    ------------
    None
    """
    line = '   ' * level + str(node.name)
    print(line)
    with open('example_tree.txt', 'a') as file:
        file.write(f'{line}\n')
    if node.children:
        for child in node.children:
            print_tree(child, level+1)
    else:
        return


def construct_state_tree(state_info, coal_data, elec_data, gas_data, temp_data, prec_data, wind_data):
    """
    Constructs a tree representation of a state's energy and weather data, using the provided data dictionaries.

    Parameters
    ------------
    state_info: dict
        A dictionary containing information about the state, such as its name and abbreviation.
    coal_data: dict
        A dictionary containing quarterly coal consumption data for the state, retrieved from the EIA API.
    elec_data: dict
        A dictionary containing monthly electricity generation data for the state, retrieved from the EIA API.
    gas_data: dict
        A dictionary containing monthly natural gas consumption data for the state, retrieved from the EIA API.
    temp_data: dict
        A dictionary containing monthly average temperature data for the state, retrieved from the NOAA API.
    prec_data: dict
        A dictionary containing monthly precipitation data for the state, retrieved from the NOAA API.
    wind_data: dict
        A dictionary containing monthly wind speed data for the state, retrieved from the NOAA API.

    Returns
    ------------
    Node:
        A tree data structure representing the state's energy and weather data
    """
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
                if len(coal_data['data']) != 0:
                    if month_node.name == coal_data['data'][coal_index]['time']:
                        month_node.add_child(coal_data['data'][coal_index]['value'])
                        coal_index -= 1
                    else:
                        month_node.add_child('None')
                else:
                    month_node.add_child('None')
                    coal_index -= 1
            except IndexError:
                month_node.add_child('None')

    elec_index = -1
    for year in range(2015, 2023):
        for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            month_node = energy.children[1].add_child(str(year) + '-' + month)
            try:
                if len(elec_data['data']) != 0:
                    if month_node.name == elec_data['data'][elec_index]['date']:
                        month_node.add_child(elec_data['data'][elec_index]['value'])
                        elec_index -= 1
                    else:
                        month_node.add_child('None')
                else:
                    month_node.add_child('None')
                    elec_index -= 1
            except IndexError:
                month_node.add_child('None')

    gas_index = -1
    for year in range(2015, 2023):
        for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            month_node = energy.children[2].add_child(str(year) + '-' + month)
            try:
                if len(gas_data['data']) != 0:
                    if month_node.name == gas_data['data'][gas_index]['date']:
                        month_node.add_child(gas_data['data'][gas_index]['value'])
                        gas_index -= 1
                    else:
                        month_node.add_child('None')
                else:
                    month_node.add_child('None')
                    gas_index -= 1
            except IndexError:
                month_node.add_child('None')

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
                    else:
                        month_node.add_child('None')
                except IndexError:
                    month_node.add_child('None')

        quar_index = 0
        for year in range(2015, 2023):
            for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
                quarter_node = weather_node.add_child(str(year) + '-' + quarter)
                try:
                    sum = 0
                    count = 0
                    for i in range(3):
                        if weather_node.children[quar_index].children[0].name != 'None':
                            sum += float(weather_node.children[quar_index].children[0].name)
                            count += 1
                        quar_index += 1
                    if count == 0:
                        quarter_node.add_child('None')
                    else:
                        avg = sum / count
                        quarter_node.add_child(round(avg, 2))
                except IndexError:
                    quarter_node.add_child('None')

    return state


def get_data_from_cache(filename):
    """
    Given a filename, reads data from a JSON file and returns it as a Python object.

    Parameters
    ------------
    filename: string
        The path of the JSON file to read.

    Returns
    ------------
    data: list
        A list representing the data read from the file.
    """
    with open(filename, 'r') as file:
        data = json.load(file)

    return data


def construct_tree():
    """
    Load data from cache and construct state trees for each state.

    The function loads state information and energy and weather data for each state from cache files.
    It then constructs a state tree for each state using the data, and adds each state tree as a
    child of a root node representing the USA.

    Parameters
    ------------
    None

    Returns
    ------------
    None
    """
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

    return root


def tree_to_json(filename):
    """
    Given a filename, writes the tree to a JSON file.

    Parameters
    ------------
    filename: string
        The path of the JSON file to write.

    Returns
    ------------
    None
    """
    tree = construct_tree()
    tree_dict = tree.to_dict()
    with open(filename, 'w') as file:
        json.dump(tree_dict, file)


if __name__ == '__main__':
    tree_to_json('tree.json')
    # tree = construct_tree()
    # lines = print_tree(tree.children[0])