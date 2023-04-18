import json
from tree import *


def from_dict(root, dict):
    """
    Recursively constructs a tree structure from a dictionary.

    Parameters
    ------------
    root: object
        The root node of the tree.
    dict: dict
        A dictionary representing the tree, as produced by the to_dict() function.

    Returns
    ------------
    Node:
        The root node of the constructed tree.
    """
    if 'children' in dict:
        for child in dict['children']:
            child_node = root.add_child(child['data'])
            from_dict(child_node, child)
    return root


def json_to_tree(filename):
    """
    Converts a JSON file to a tree of nodes.

    Parameters
    ------------
    filename: string
        The path to the JSON file.

    Returns
    ------------
    The root node of the resulting tree.
    """
    with open(filename, 'r') as file:
        tree_dict = json.load(file)
    root = Node(tree_dict['data'])
    tree = from_dict(root, tree_dict)
    return tree