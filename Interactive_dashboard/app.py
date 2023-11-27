from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import filter
from chart_updater import bar_chart
from update_pie import pie_chart_updater
from update_map import map_updater

# Read the Excel file and get sheet names
excel_file = pd.ExcelFile('Summary of SAS.xlsx')
sheet_names = excel_file.sheet_names

other_file = pd.ExcelFile('other_findings.xlsx')
sheets = other_file.sheet_names

detailed_file = pd.ExcelFile('Detailed_sas_file.xlsx')
detailed_sheets = detailed_file.sheet_names

# Initialize lists for indicators and years
indicators = filter.filter_indicators(excel_file)
years = ['SAS 2020', 'SAS 2021', 'SAS 2022']

detailed_indicators = filter.filter_indicators(detailed_file)

# Create a Dash app instance
app = Dash(__name__)

p = """
This Dashboard highlights the findings of the Seasonal Agricultural Survey (SAS) for the agricultural year 
2021/2022. It covers three agricultural seasons; Season A which starts from September to February of the 
following year and Season B which starts from March to June. Season C is the shortest agricultural season 
with vegetables and sweet potato predominantly grown in swamps and Irish potato mostly grown in the 
volcanic agro-ecological zone. This dashboard highlights mainly these:
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
                    html.H1(children='SEASONAL AGRICULTURAL SURVEY (SAS)', style={'textAlign': 'center'}),
                    html.H3(children='EXECUTIVE SUMMARY', style={'textAlign': 'center'})
                ],
                style={'padding-left': '350px'}
            )
        ],
        style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start'}
    ),
    html.Div([
        html.P(p),
        html.Ul([
            html.Li(item) for item in item_list
        ]),
        html.P("The bar chart below illustrates the summary of Seasonal Agricultural Survey main indicators for the last three years.")
    ]),
    html.Label('Choose year:'),
    dcc.RadioItems(options=years, value=years[0], inline=True, id='year-dropdown'),
    html.Label('Choose the indicator of your interest:'),
    dcc.Dropdown(
        id='indicator-dropdown',
        options=[{'label': indicator, 'value': indicator} for indicator in indicators],
        value=indicators[0], style={'width': '500px', 'height': '40px'}
    ),
    dcc.Graph(figure={}, id='bar-chart-1'),
    html.Label('Choose year:'),
    dcc.RadioItems(options=[2021, 2022], value=2021, inline=True, id='years-dropdown'),
    html.Label('Choose the data of your interest:'),
    dcc.Dropdown(
        id='names',
        options={},
        value="", style={'width': '500px', 'height': '40px'}
    ),
    dcc.Graph(figure={}, id='pie-charts-1'),
    html.P('The following figures demonstrates the findngs of the seasonal agricultural survey in every distict of Rwanda in the 2022.'),
    html.P('You can explore the findings in every district of Rwanda by hovering over the the district of interest on the following maps of Rwanda generated based on agricultural seasons.'),
    html.Label('Choose the indicator:'),
    dcc.Dropdown(
        id='detailed_indicator',
        options=[{'label': detailed_indicator, 'value': detailed_indicator} for detailed_indicator in detailed_indicators],
        value=detailed_indicators[0], style={'width': '500px', 'height': '40px'}
    ),
    html.Label('Choose the dataset of your interest:'),
    dcc.Dropdown(
        id='chosen_detailed_indicator',
        options={},
        value="",
        style={'width': '500px', 'height': '40px'}
    ),

    dcc.Graph(figure={}, id='detailed-chart-1'),
    dcc.Graph(figure={}, id='detailed-chart-2'),
    dcc.Graph(figure={}, id='detailed-chart-3')
], style={'margin': '30px', 'font-family': 'Cambria, "Times New Roman", serif', 'font-size': '16px'})

bar_chart(app, excel_file, other_file)

pie_chart_updater(app, other_file)

map_updater(app, detailed_file)



if __name__ == '__main__':
    app.run_server(debug=True)