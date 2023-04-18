import plotly.graph_objects as go

def bar_chart(data, states, title, unit):
    """
    This function creates a bar chart using the Plotly library, given the input data and specifications.

    Parameters
    ------------
    data: list / object
        A list or an object of the ElementTree class from the xml.etree.ElementTree module.
        If data is a list, it must contain objects of the BeautifulSoup class.
        If data is an ElementTree object, it represents an XML document.
    states: list
        A list of strings representing the names of states. Only applicable if data is a list.
    title: string
        A string representing the title of the chart.
    unit: string
        A string representing the unit of measurement for the y-axis.

    Returns
    ------------
    chart_div: string
        A string containing the HTML code for the chart.
    """
    if isinstance(data, list):
        x_values = states
        y_values = []
        for item in data:
            y_values.append(item.children[0].name)
    else:
        x_values = []
        y_values = []
        if len(data.children) == 1:
            x_values.append(data.name)
            y_values.append(data.children[0].name)

        else:
            for child in data.children:
                x_values.append(child.name)
                y_values.append(child.children[0].name)

    fig = go.Figure(data=[go.Bar(x=x_values, y=y_values, name=title)])

    fig.update_layout(title=title, yaxis_title=f'Units: {unit}')

    chart_div = fig.to_html(full_html=False)

    return chart_div


def two_bar_chart(data1, data2, states, title, name1, name2, unit1, unit2):
    """
    This function creates a two-bar chart using the Plotly library, given the input data and specifications.

    Parameters
    ------------
    data1: list / object
        A list or an object of the ElementTree class from the xml.etree.ElementTree module.
            If data1 is a list, it must contain objects of the BeautifulSoup class.
            If data1 is an ElementTree object, it represents an XML document.
    data2: list / object
        A list or an object of the ElementTree class from the xml.etree.ElementTree module.
            If data2 is a list, it must contain objects of the BeautifulSoup class.
            If data2 is an ElementTree object, it represents an XML document.
    states: list
        A list of strings representing the names of states. Only applicable if data1 is a list.
    title: string
        A string representing the title of the chart.
    name1: string
        A string representing the name of the first bar in the chart.
    name2: string
        A string representing the name of the second bar in the chart.
    unit1: string
        A string representing the unit of measurement for the y-values of the first bar.
    unit2: string
        A string representing the unit of measurement for the y-values of the second bar.

    Returns
    ------------
    chart_div: string
        A string containing the HTML code for the chart.
    """
    if isinstance(data1, list):
        x_values = states
        y_values1 = []
        y_values2 = []
        for item in data1:
            if item.children[0].name is None or item.children[0].name == 'None':
                y_values1.append(0)
            else:
                y_values1.append(item.children[0].name)
        for item in data2:
            if item.children[0].name is None or item.children[0].name == 'None':
                y_values2.append(0)
            else:
                y_values2.append(item.children[0].name)
    else:
        x_values = []
        y_values1 = []
        y_values2 = []
        if len(data1.children) == 1:
            x_values.append(data1.name)
            y_values1.append(data1.children[0].name)
            y_values2.append(data2.children[0].name)

        else:
            for child in data1.children:
                x_values.append(child.name)
                if child.children[0].name is None or child.children[0].name == 'None':
                    y_values1.append(0)
                else:
                    y_values1.append(child.children[0].name)
            for child in data2.children:
                if child.children[0].name is None or child.children[0].name == 'None':
                    y_values2.append(0)
                else:
                    y_values2.append(child.children[0].name)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_values, y=[value/1000 for value in y_values1], base=0, marker_color='#065C38', name=name1))
    fig.add_trace(go.Bar(x=x_values, y=y_values2, base=[-value for value in y_values2], marker_color='lightslategrey', name=name2))

    fig.update_layout(title=title, yaxis=dict(showticklabels=False, automargin=True), yaxis_title=f'{unit1}    {unit2}')

    chart_div = fig.to_html(full_html=False)

    return chart_div