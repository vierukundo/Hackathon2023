from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json
import numpy as np

# Read the Excel file and get sheet names
excel_file = pd.ExcelFile('Summary of SAS.xlsx')
sheet_names = excel_file.sheet_names

other_file = pd.ExcelFile('other_findings.xlsx')
sheets = other_file.sheet_names

detailed_file = pd.ExcelFile('Detailed_sas_file.xlsx')
detailed_sheets = detailed_file.sheet_names


# read the Rwanda geojson file
with open('rwanda_geojson.geojson', 'r') as f:
    Rwanda_districts = json.load(f)

district_id_map = {}
for feature in Rwanda_districts['features']:
    feature['id'] = str(feature['properties']['ID_2'])
    district_id_map[feature['properties']['NAME_2']] = feature['id']  # Convert to string


# Initialize lists for indicators and years
indicators = []
years = []

# Iterate through the sheets to gather indicator and year data
for sheet_name in sheet_names:
    df = excel_file.parse(sheet_name)
    indicators.append(df.columns[0])
    years.append(df.columns[4])

detailed_indicators = []
for d_sheet in detailed_sheets:
    df = detailed_file.parse(d_sheet)
    if df.columns[0] not in detailed_indicators:
        detailed_indicators.append(df.columns[0])

# Create a Dash app instance
app = Dash(__name__)

# Remove duplicates from the lists
years = list(set(years))
indicators = list(set(indicators))

p2 = """
This report highlights the findings of the Seasonal Agricultural Survey (SAS) for the agricultural year 
2021/2022. It covers three agricultural seasons; Season A which starts from September to February of the 
following year and Season B which starts from March to June. Season C is the shortest agricultural season 
with vegetables and sweet potato predominantly grown in swamps and Irish potato mostly grown in the 
volcanic agro-ecological zone. This report, therefore, consolidates the findings of all seasons and hence, 
highlights the findings mainly related to:
"""
p1 = """
Agriculture plays a pivotal role in Rwanda's economic growth, and it is a key focus of the national development strategy. 
The government has set an ambitious agenda for agricultural transformation, aiming to shift from low productivity to knowledge-driven, value-added, 
and commercialized agriculture. Accurate agricultural statistics are crucial for monitoring national programs and making informed decisions. 
The National Institute of Statistics of Rwanda, in partnership with the Ministry of Agriculture and Animal Resources, conducts the Seasonal 
Agricultural Survey (SAS) to gather vital agricultural information.
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
        html.P(p1),
        html.P(p2),
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
], style={'margin': '40px', 'font-family': 'Cambria, "Times New Roman", serif', 'font-size': '16px'})

@app.callback(
    Output('bar-chart-1', 'figure'),
    [Input('year-dropdown', 'value'), Input('indicator-dropdown', 'value')]
)
def chart_updater(chosen_year, chosen_indicator):
    figure = make_subplots(rows=1, cols=2, specs=[[{'type': 'xy'}, {'type': 'xy'}]], subplot_titles=("Indicator", "Rwanda Land cover classes"))
    for sheet_name in sheet_names:
        df = excel_file.parse(sheet_name)
        if df.columns[0] == chosen_indicator and df.columns[4] == chosen_year:
            break

    # Create a bar chart with multiple y-values
    figure.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[1]], name=df.columns[1]), row=1, col=1)
    figure.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[2]], name=df.columns[2]), row=1, col=1)
    figure.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[3]], name=df.columns[3]), row=1, col=1)

    df2 = other_file.parse('Sheet1')
    figure2 = go.Bar(x=df2[df2.columns[0]], y=df2[df2.columns[1]])
    
    figure.add_trace(figure2, row=1, col=2)
    figure.update_layout(
        title_text=f'{chosen_year} - {chosen_indicator} in Seasons A, B, and C'
    )
    return figure

@app.callback(
    [Output('names', 'options'), Output('names', 'value')],
    Input('years-dropdown', 'value')
)
# this updates the dropdown with dataset of selected indicator
def check_year(year):
    names = []
    if year == 2021:
        new_sheets = sheets[1:13]
    else:
        new_sheets = sheets[1:]
    for sh_name in new_sheets:
        df = other_file.parse(sh_name)
        if df.columns[0] not in names:
            names.append(df.columns[0])
    options = [{'label': name, 'value': name} for name in names]
    return options, names[0]

@app.callback(
    Output('pie-charts-1', 'figure'),
    [Input('years-dropdown', 'value'), Input('names', 'value')]
)
# This updates the piecharts according to year and dataset selected
def pie_updater_one(year, name):
    fig_pie = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]], subplot_titles=("Season A", "Season B", "Season C"))
    for sheet in sheets[1:]:
        pie_df = other_file.parse(sheet)
        if pie_df.columns[0] == name and year in pie_df.columns and 'Season A' in pie_df.columns:
            fig_pie.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[pie_df.columns[1]].tolist()), 1, 1)
        elif pie_df.columns[0] == name and year in pie_df.columns and 'Season B' in pie_df.columns:
            fig_pie.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[pie_df.columns[1]].tolist()), 1, 2)
        elif pie_df.columns[0] == name and year in pie_df.columns and 'Season C' in pie_df.columns:
            fig_pie.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[pie_df.columns[1]].tolist()), 1, 3)
            break
    if fig_pie:
        fig_pie.update_layout(title_text=name)
        fig_pie.update_traces(textposition='inside')
    return fig_pie


@app.callback(
    [Output('chosen_detailed_indicator', 'options'), Output('chosen_detailed_indicator', 'value')],
    Input('detailed_indicator', 'value')
)
# this updates the dropdown with dataset of selected indicator
def update_drop_down(detailed_indicator):
    for sheet in detailed_sheets:
        detailed_df = detailed_file.parse(sheet)
        if detailed_df.columns[0] == detailed_indicator:
            options = [{'label': indicator, 'value': indicator} for indicator in detailed_df.columns[1:-1]]
            return options, detailed_df.columns[1]

@app.callback(
    [Output('detailed-chart-1', 'figure'), Output('detailed-chart-2', 'figure'), Output('detailed-chart-3', 'figure')],
    [Input('chosen_detailed_indicator', 'value'), Input('detailed_indicator', 'value')]
)
# This function updates the rwandan maps according to selected dataset
def update_detailed_charts(indicator, detailed_indicator):
    figure1, figure2, figure3 = None, None, None
    for sheet in detailed_sheets[:13]:
        detailed_f = detailed_file.parse(sheet)
        if detailed_f.columns[0] == detailed_indicator and 'Season A' in detailed_f.columns:
            detailed_f['Density'] = pd.to_numeric(detailed_f[indicator], errors='coerce').apply(lambda x: np.log10(int(x) if not np.isnan(x) else 0))
            detailed_f['id'] = detailed_f[detailed_f.columns[0]].apply(lambda x: district_id_map.get(x, None))
            detailed_f = detailed_f.rename(columns={detailed_f.columns[0]: 'District'})    
            figure1 = px.choropleth_mapbox(detailed_f, geojson=Rwanda_districts, locations='id', color='Density', hover_data=['Density', indicator, detailed_f.columns[0]],
                                    mapbox_style="carto-positron", center={"lat": -1.9403, "lon": 29.8739}, zoom=7)
            figure1.update_layout(title=f'{indicator} in Season A')
        elif detailed_f.columns[0] == detailed_indicator and 'Season B' in detailed_f.columns:
            detailed_f['Density'] = pd.to_numeric(detailed_f[indicator], errors='coerce').apply(lambda x: np.log10(int(x) if not np.isnan(x) else 0))
            detailed_f['id'] = detailed_f[detailed_f.columns[0]].apply(lambda x: district_id_map.get(x, None))
            detailed_f = detailed_f.rename(columns={detailed_f.columns[0]: 'District'})
            figure2 = px.choropleth_mapbox(detailed_f, geojson=Rwanda_districts, locations='id', color='Density', hover_data=['Density', indicator, detailed_f.columns[0]],
                                    mapbox_style="carto-positron", center={"lat": -1.9403, "lon": 29.8739}, zoom=7)
            figure2.update_layout(title=f'{indicator} in Season B')
        elif detailed_f.columns[0] == detailed_indicator and 'Season C' in detailed_f.columns:
            detailed_f['Density'] = pd.to_numeric(detailed_f[indicator], errors='coerce').apply(lambda x: np.log10(int(x) if not np.isnan(x) else 0))
            detailed_f['id'] = detailed_f[detailed_f.columns[0]].apply(lambda x: district_id_map.get(x, None))
            detailed_f = detailed_f.rename(columns={detailed_f.columns[0]: 'District'})
            figure3 = px.choropleth_mapbox(detailed_f, geojson=Rwanda_districts, locations='id', color='Density', hover_data=['Density', indicator, detailed_f.columns[0]],
                                    mapbox_style="carto-positron", center={"lat": -1.9403, "lon": 29.8739}, zoom=7)
            figure3.update_layout(title=f'{indicator} in Season C')
            break
    return figure1, figure2, figure3



if __name__ == '__main__':
    app.run_server(debug=True)