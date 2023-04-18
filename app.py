from flask import Flask, render_template, request, url_for, redirect
import json

from json_to_tree import *
from data_search import *
from line_chart import *
from bar_chart import *
from get_units import *

app = Flask(__name__)

tree = json_to_tree('tree.json')

@app.route("/", methods=['GET', 'POST'])
def index():
    with open('state info.json', 'r') as file:
        data = json.load(file)
    states = [state['state'] for state in data]

    months = []
    for year in range(2015, 2023):
        for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            month = str(year) + '-' + month
            months.append(month)

    quats = []
    for year in range(2015, 2023):
        for quat in ['Q1', 'Q2', 'Q3', 'Q4']:
            quat = str(year) + '-' + quat
            quats.append(quat)

    units = get_unit()

    if request.method == 'POST':
        state = request.form['state']
        energy_type = request.form['energy_type']
        weather_type = request.form['weather_type']
        presentation_type = request.form['presentation_type']

        if energy_type == 'coal':
            energy_unit = units[0]
            time = request.form['quarter']
        elif energy_type == 'electricity':
            energy_unit = units[1]
            time = request.form['month']
        elif energy_type == 'natural gas':
            energy_unit = units[2]
            time = request.form['month']
        else:
            time = request.form['month']

        if weather_type == 'temperature':
            weather_unit = units[3]
        elif weather_type == 'precipitation':
            weather_unit = units[4]
        elif weather_type == 'wind':
            weather_unit = units[5]

        energy_data = []
        weather_data = []

        if state != '':
            if energy_type != '':
                energy_data = search_from_state(tree, state, energy_type, time)
            if weather_type != '':
                weather_data = search_from_state(tree, state, weather_type, time)
            if energy_type == '' and weather_type == '':
                return render_template("index.html", states=states, months=months, quats=quats)

            if presentation_type == 'table':
                return render_template('table.html', energy_type=energy_type, weather_type=weather_type, data1=energy_data, data2=weather_data)

            if presentation_type == 'line':
                if energy_type != '' and weather_type == '':
                    title = f'{state} {energy_type} Data'
                    chart_div = [generate_line_chart(energy_data, states, title, energy_unit)]
                if energy_type == '' and weather_type != '':
                    title = f'{state} {weather_type} Data'
                    chart_div = [generate_line_chart(weather_data, states, title, weather_unit)]
                if energy_type != '' and weather_type != '':
                    title = f'{state} {energy_type} & {weather_type} Comparison'
                    chart_div1, chart_div2 = generate_two_line_chart(energy_data, weather_data, states, title, energy_type, weather_type, energy_unit, weather_unit)
                    chart_div = [chart_div1, chart_div2]
                return render_template('line_chart.html', chart_div=chart_div)

            if presentation_type == 'bar':
                if energy_type != '' and weather_type == '':
                    title = f'{state} {energy_type} Data'
                    chart_div = bar_chart(energy_data, states, title, energy_unit)
                if energy_type == '' and weather_type != '':
                    title = f'{state} {weather_type} Data'
                    chart_div = bar_chart(weather_data, states, title, weather_unit)
                if energy_type != '' and weather_type != '':
                    title = f'{state} {energy_type} & {weather_type} Comparison'
                    chart_div = two_bar_chart(energy_data, weather_data, states, title, energy_type, weather_type, unit1=weather_unit, unit2=f'Thousand {energy_unit}')
                return render_template('bar_chart.html', chart_div=chart_div)


        else:
            if time != '':
                if energy_type != '':
                    energy_data = search_from_type(tree, energy_type, time)
                if weather_type != '':
                    weather_data = search_from_type(tree, weather_type, time)
            else:
                return render_template("index.html", states=states, months=months, quats=quats)

            if presentation_type == 'table':
                return render_template('table2.html',states=states, energy_type=energy_type, weather_type=weather_type, data1=energy_data, data2=weather_data, time=time)

            if presentation_type == 'line':
                if energy_type != '' and weather_type == '':
                    title = f'{time} {energy_type} Data'
                    chart_div = [generate_line_chart(energy_data, states, title, energy_unit)]
                if energy_type == '' and weather_type != '':
                    title = f'{time} {weather_type} Data'
                    chart_div = [generate_line_chart(weather_data, states, title, weather_unit)]
                if energy_type != '' and weather_type != '':
                    title = f'{time} {energy_type} & {weather_type} Comparison'
                    chart_div1, chart_div2 = generate_two_line_chart(energy_data, weather_data, states, title, energy_type, weather_type, energy_unit, weather_unit)
                    chart_div = [chart_div1, chart_div2]
                return render_template('line_chart.html', chart_div=chart_div)

            if presentation_type == 'bar':
                if energy_type != '' and weather_type == '':
                    title = f'{state} {energy_type} Data'
                    chart_div = bar_chart(energy_data, states, title, energy_unit)
                if energy_type == '' and weather_type != '':
                    title = f'{state} {weather_type} Data'
                    chart_div = bar_chart(weather_data, states, title, weather_unit)
                if energy_type != '' and weather_type != '':
                    title = f'{state} {energy_type} & {weather_type} Comparison'
                    chart_div = two_bar_chart(energy_data, weather_data, states, title, energy_type, weather_type, unit1=weather_unit, unit2=f'Thousand {energy_unit}')
                return render_template('bar_chart.html', chart_div=chart_div)


    return render_template("index.html", states=states, months=months, quats=quats)


@app.route('/back')
def back():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)