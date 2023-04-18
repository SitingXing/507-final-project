import plotly.graph_objects as go

def generate_line_chart(data, states, title, unit):
    """
    Generate a line chart using the Plotly library based on the input data.

    Parameters
    ------------
    data: list / object
        the data to be plotted; a node or a list of nodes
    states: list
        a list of strings representing the states or time periods to be plotted on the x-axis
    title: string
        a string representing the title of the chart
    unit: string
        a string representing the unit of measurement for the y-axis values

    Returns
    ------------
    chart_div: string
        a string representing the HTML code for the generated chart
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

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', name=title))

    fig.update_layout(title=title, xaxis_title='Time Period', yaxis_title=f'Units: {unit}', showlegend=True)

    chart_div = fig.to_html(full_html=False)

    return chart_div


def generate_two_line_chart(data1, data2, states, title, name1, name2, unit1, unit2):
    """
    Generate two line charts with separate y-axes on the same figure.

    Parameters:
    -----------
    data1 : Node or list
        The data to be plotted on the first chart.
    data2 : Node or list
        The data to be plotted on the second chart.
    states : list
        The x-axis labels for both charts.
    title : string
        The title of the chart.
    name1 : string
        The name of the data series plotted on the first chart.
    name2 : string
        The name of the data series plotted on the second chart.
    unit1 : string
        The unit of measurement for the data series plotted on the first chart.
    unit2 : string
        The unit of measurement for the data series plotted on the second chart.

    Returns:
    --------
    chart_div1 : string
        A string containing the HTML for the first chart.
    chart_div2 : string
        A string containing the HTML for the second chart.
    """
    if isinstance(data1, list):
        x_values1 = states
        x_values2 = states
        y_values1 = []
        y_values2 = []
        for item in data1:
            y_values1.append(item.children[0].name)
        for item in data2:
            y_values2.append(item.children[0].name)
    else:
        x_values1 = []
        x_values2 = []
        y_values1 = []
        y_values2 = []
        if len(data1.children) == 1:
            x_values1.append(data1.name)
            x_values2.append(data1.name)
            y_values1.append(data1.children[0].name)
            y_values2.append(data2.children[0].name)

        else:
            for child in data1.children:
                x_values1.append(child.name)
                y_values1.append(child.children[0].name)
            for child in data2.children:
                x_values2.append(child.name)
                y_values2.append(child.children[0].name)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=x_values1, y=y_values1, mode='lines+markers', name=name1))
    layout1 = go.Layout(title_text=title, margin=dict(t=0, b=0, l=0, r=0), xaxis=dict(showticklabels=False), width=1000, height=300, yaxis=dict(showticklabels=False, automargin=True), yaxis_title=f'Units: {unit1}', showlegend=True, legend=dict(yanchor='bottom', y=0, xanchor='right', x=1))

    fig1.update_layout(layout1)

    chart_div1 = fig1.to_html(full_html=False)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=x_values2, y=y_values2, mode='lines+markers', line_color='#065C38', name=name2))
    layout2 = go.Layout(margin=dict(t=0, b=0, l=0, r=0), width=1000, height=300, yaxis=dict(showticklabels=False, automargin=True), yaxis_title=f'Units: {unit2}', showlegend=True, legend=dict(yanchor='bottom', y=0, xanchor='right', x=1))

    fig2.update_layout(layout2)

    chart_div2 = fig2.to_html(full_html=False)

    return chart_div1, chart_div2