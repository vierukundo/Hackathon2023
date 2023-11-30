from dash import Dash, html, dcc
import pandas as pd
import dash
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import filter
from chart_updater import bar_chart
from update_pie import pie_chart_updater
from update_map import map_updater

# Read the Excel file and get sheet names
summary_file = pd.ExcelFile('Summary of SAS.xlsx')
sheet_names = summary_file.sheet_names

other_file = pd.ExcelFile('other_findings.xlsx')
sheets = other_file.sheet_names

detailed_file = pd.ExcelFile('Detailed_sas_file.xlsx')
detailed_sheets = detailed_file.sheet_names

# Initialize lists for indicators and years
indicators = filter.filter_indicators(summary_file)
years = ['SAS 2020', 'SAS 2021', 'SAS 2022']

detailed_indicators = filter.filter_indicators(detailed_file)

# Create a Dash app instance
app = dash.Dash(__name__)

p = """
This Dashboard highlights the findings of the Seasonal Agricultural Survey (SAS) for the agricultural year 
2021/2022. It covers three agricultural seasons; Season A which starts from September to February of the 
following year and Season B which starts from March to June. Season C is the shortest agricultural season 
with vegetables and sweet potato predominantly grown in swamps and Irish potato mostly grown in the 
volcanic agro-ecological zone. This dashboard highlights mainly:
"""

p2 = "This section delves into additional insights from the seasonal agricultural survey, expanding beyond the scope of the core indicators."

p3 = """
Embark on a visual journey through Rwanda's agricultural landscape by exploring the interactive maps below.
Each map highlights thefindings of the seasonal agricultural survey across every district in 2022, providing a comprehensive overview of crop yields, input utilization, and other key agricultural indicators.
"""
item_list = [
    "Land use", "Crop land", "Crop production",
    "Crop yield", "Use of inputs", "Agricultural practices"
]
# Define the layout of the web application
app.layout = html.Div([
    html.Div(
        [
            html.Div(html.Img(src=app.get_asset_url('NISR-logo.jpg'), style={'width': '100px', 'height': '100px'})),
            html.Div(
                [
                    html.H1(children='SEASONAL AGRICULTURAL SURVEY (SAS)', style={'textAlign': 'center'})
                ],
                style={'padding-left': '200px'}
            )
        ],
        style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start'}
    ),
    html.Div([
        html.P(p),
        html.Ul([
            html.Li(item) for item in item_list
        ], className="list"),
        html.H3("This section consists of interactive bar chart that illustrates the summary of Seasonal Agricultural Survey main indicators for the last three years.")
    ]),
    html.Label('Choose year:', className="labels"), html.Br(),
    dcc.RadioItems(options=years, value=years[0], inline=True, id='year-dropdown', className="radio_items"), html.Br(),
    html.Label('Choose the indicator of your interest:', className="labels"), html.Br(),
    dcc.Dropdown(
        id='indicator-dropdown',
        options=[{'label': indicator, 'value': indicator} for indicator in indicators],
        className="dropdowns",
        value=indicators[0]
    ),
    dcc.Graph(figure={}, id='bar-chart-1'),
    html.H3(p2),
    html.Label('Choose year:', className="labels"), html.Br(),
    dcc.RadioItems(options=[2021, 2022], value=2021, inline=True, id='years-dropdown', className="radio_items"), html.Br(),
    html.Label('Choose the indicator of your interest:', className="labels"), html.Br(),
    dcc.Dropdown(
        id='names',
        options={},
        className="dropdowns",
        value=""
    ),
    html.Label('Choose the data of your interest:', className="labels"),
    dcc.Dropdown(
        id='data',
        options={},
        value="",
        className="dropdowns"
    ),
    dcc.Graph(figure={}, id='pie-charts-1'),
    html.H3("This section demostrates agricultural performance across Rwanda's districts in 2022."),
    html.P(p3),
    html.H4("Hover over each map to explore the findings!"),
    html.Label('Choose the indicator:', className="labels"),
    dcc.Dropdown(
        id='detailed_indicator',
        options=[{'label': detailed_indicator, 'value': detailed_indicator} for detailed_indicator in detailed_indicators],
        value=detailed_indicators[0],
        className="dropdowns"
    ),
    html.Label('Choose the dataset of your interest:', className="labels"),
    dcc.Dropdown(
        id='chosen_detailed_indicator',
        options={},
        value="",
        className="dropdowns"
    ),

    dcc.Graph(figure={}, id='detailed-chart-1'),
    dcc.Graph(figure={}, id='detailed-chart-2'),
    dcc.Graph(figure={}, id='detailed-chart-3')
], style={'margin': '30px', 'font-family': 'Cambria, "Times New Roman", serif', 'font-size': '16px'})

bar_chart(app, summary_file)
pie_chart_updater(app, other_file)
map_updater(app, detailed_file)


if __name__ == '__main__':
    app.run_server(debug=True)