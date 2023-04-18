<h1>507 Final Project</h1>
<h4>Siting Xing</h4>

<h2>Description</h2>
This project is a Flask web application that allows users to generate tables and graphs showing the data and relationship between energy consumption and weather patterns. Specifically, users can select from three energy sources (coal, electricity, and natural gas) and three weather patterns (temperature, precipitation, and wind) to generate a customized graph using the Plotly library.

The application includes a form with dropdown menu where users can select their desired state, energy source, weather pattern, and time period. Once the user submits their selections, the Flask app passes these information to a Python script that retrieves the relevant data and formats it appropriately for Plotly.

The resulting graph is displayed within the Flask app using Plotly's interactive visualization tools, allowing users to explore the data further by hovering over data points, zooming in/out, and more.

Overall, this project is a useful tool for analyzing the relationship between energy consumption and weather patterns, and the Flask and Plotly libraries provide a powerful and user-friendly platform for creating and sharing these visualizations.

<h2>Instructions</h2>
<h3>Run project</h3>
To run a Python code from this GitHub repo:

1. Download the code: Go to the GitHub repository and click on the "Code" button. From the dropdown menu, select "Download ZIP" to download the entire repository as a zip file. Alternatively, you can copy the repository's URL and clone it using Git by running the command git clone <repository_URL> in the terminal. Make sure that all files and folders are in the same folder or the same directory.

2. Install dependencies: Once you have downloaded the code, navigate to the project directory using the terminal and install any necessary dependencies in the below package list by running the command pip install.

3. Run the code: To run the project, open and start app.py file either in terminal with command python app.py or in code editer (for example, vscode). Flask environment will become active. i.e. Terminal should show something like below.
Running on http://127.0.0.1:5000/
(Press CTRL+C to quit)
Copy or type the link to the browser to view the interface.

<h3>Interface Interaction</h3>
The Flask app in this project includes a user interface that allows users to interact with the application and generate customized tables and graphs based on their selections. There are 5 options in the interface for users to select: state, energy, weather, time, and presentation mode. Each option has a drop-down menu to choose from: all 50 states in U.S., 3 types of energy (coal, electricity, natural gas), 3 types of weather pattern (temperature, precipitation, wind), 2 sets for time (month, quarter), and 3 types of presentation (table, line chart, bar chart).

1. Select options: The user selects their desired options by clicking in the options with dropdown menus. Users need to choose one presentation type to be able to submit the form (click the "Search" button). Users can customize other options with at least 2 options selected. If users give an invalid form, the app will send back to the search (form) page to let users try another option combination.

2. View results: The Flask app generates the table and graph using Plotly's visualization tools based on users' options and displays it to the user within the application. The user can interact with the graph by hovering over data points, zooming in/out, and more.

3. Save or share graph: Users have the option to save the generated graph. For example, the user is able to download the graph as an image.

4. Back to generate new search: Users can click on the "Back to Search" button at the top right corner to go back to the search page and generate new searching.

<h3>Supply API Key</h3>
The data used in this project have been all cached into json files, and provided inside the repo. Also, data used to construct the flask app are from cache files. So, typically, if only running the project, there is no need for new api key or token. 

However, if there is a special need (for example, for different or new time period), you can update the api key and token.
1. Get api key and token for two api: EIA api -- https://www.eia.gov/opendata/index.php to register an account; NOAA api -- https://www.ncdc.noaa.gov/cdo-web/token to request a token.
2. Update key and token: Copy your own api key and token into file API_key.txt. Update the time period you want with the format "yyyy-mm-dd".
3. Get new data and cache files: Run the following code files: coal data.py, electricity data.py, natural gas data.py, weather data.py. The new cache files can be found in folder: energy_data_cache, weather_data_cache.

<h3>Other Special Instructions</h3>
  1. If getting new data from api, because both api dataset used in the project have a large load on data accessing, there will be error happening if fetching too much data. So the code is set to wait 60 sec and try again if there is too frequent request error happened to allow fetching all data needed. The program will print out "wait" to indicate the issue.

2. The NOAA API may be down sometimes. Please check the NOAA website status for the situation.

<h2>Required Packages</h2>
<ul>
  <li>Flask</li>
  <li>plotly</li>
</ul>

<h2>Data Structure</h2>
The project uses a tree data structure to organize data from two api.
The tree data structure consisting of several nodes connected by edges. The top is the root node, which is USA. It has 50 child nodes below it, which are 50 states. Each state has 2 child nodes, one energy node, one weather node. Energy node has 3 children for 3 energy types – coal, electricity, and natural gas. Weather node has 3 children for 3 weather data types – temperature, precipitation, and wind. Each of these child nodes have 96 child nodes for each month from 2015 to 2022 and sub-child for the value of the data, except coal data which is separated by quarters with 32 child nodes for each quarter from 2015 to 2022. Basically, the tree is like below:
<ul>
  <li>
    USA
    <ul>
      <li>
        Alabama
        <ul>
          <li>
            Energy
            <ul>
              <li>
                Coal
                <ul>
                  <li>
                    2015-Q1
                    <ul>
                      <li>value</li>
                    </ul>
                  </li>
                  <li>…</li>
                  <li>
                    2022-Q4
                    <ul>
                      <li>value</li>
                    </ul>
                  </li>
                </ul>
              </li>
              <li>
                Electricity
                <ul>
                  <li>2015-01</li>
                  <li>…</li>
                  <li>2022-12</li>
                </ul>
              </li>
              <li>
                Natural gas
                <ul>
                  <li>2015-01</li>
                  <li>…</li>
                  <li>2022-12</li>
                </ul>
              </li>
            </ul>
          </li>
          <li>
            Weather
            <ul>
              <li>
                Temperature
                <ul>
                  <li>2015-01</li>
                  <li>…</li>
                  <li>2022-12</li>
                </ul>
              </li>
              <li>
                Precipitation
                <ul>
                  <li>2015-01</li>
                  <li>…</li>
                  <li>2022-12</li>
                </ul>
              </li>
              <li>
                Wind
                <ul>
                  <li>2015-01</li>
                  <li>…</li>
                  <li>2022-12</li>
                </ul>
              </li>
            </ul>
          </li>
        </ul>
      </li>
      <li>
        Alaska
      </li>
      <li>
        …
      </li>
    </ul>
  </li>
</ul>
