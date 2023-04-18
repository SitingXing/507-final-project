def search(node, value):
    """
    This function recursively searches for a node with the given value in a tree, represented as a Node object.

    Parameters
    ------------
    node: object
        A Node object representing the root node of the tree to search.
    value: string
        A string representing the value to search for.

    Returns
    ------------
    result: object
        A Node object representing the first node in the tree that has the given value, if found.
              Returns None if the value is not found in the tree.
    """
    if node is None:
        return None
    if node.name == value:
        return node
    for child in node.children:
        result = search(child, value)
        if result is not None:
            return result


def search_from_state(tree, state, value, time):
    """
    This function searches for a node with the given value in a tree, starting from a node representing a state.
    The state node is located in the tree using a search function. If a node with the given value is found in the
    state subtree, it is returned. If a time value is provided, the function searches for a node with the given value
    and time in the state subtree.

    Parameters
    ------------
    tree: object
        A Node object representing the root node of the tree to search.
    state: string
        A string representing the value of the state node to start the search from.
    value: string
        A string representing the value to search for.
    time: string
        A string representing a time value to search for. If empty, the function searches for the node without regard to time.

    Returns
    ------------
    result: object
        A Node object representing the first node in the state subtree that has the given value.
              Returns None if the value is not found in the state subtree.
    result_with_time: object
        A Node object representing the first node in the state subtree that has the given value and time. Returns None if the value and time are not found in the state subtree.
    """
    state_tree = search(tree, state)
    result = search(state_tree, value)
    if time == '':
        return result
    else:
        result_with_time = search(result, time)
        return result_with_time


def search_from_type(tree, type, time):
    """
    This function searches for nodes with the given type value in a tree, and returns a list of nodes that have the type value.
    If a time value is provided, the function searches for nodes with the given type and time in the tree.

    Parameters
    ------------
    tree: object
        A Node object representing the root node of the tree to search.
    type: string
        A string representing the value of the type to search for.
    time: string
        A string representing a time value to search for. If empty, the function searches for nodes without regard to time.

    Returns
    ------------
    results: list
        A list of Node objects representing all nodes in the tree that have the given type value.
               Returns an empty list if no nodes are found with the type value.
    """
    results = []
    for node in tree.children:
        result = search(node, type)
        result_with_time = search(result, time)
        results.append(result_with_time)
    return results