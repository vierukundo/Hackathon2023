from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Read the Excel file and get sheet names
excel_file = pd.ExcelFile('Summary of SAS.xlsx')
sheet_names = excel_file.sheet_names

other_file = pd.ExcelFile('other_findings.xlsx')
sheets = other_file.sheet_names
# Initialize lists for indicators and years
indicators = []
years = []

# Iterate through the sheets to gather indicator and year data
for sheet_name in sheet_names:
    df = excel_file.parse(sheet_name)
    indicators.append(df.columns[0])
    years.append(df.columns[4])

names = []
crops = []
for sh_name in sheets[1:]:
    df = other_file.parse(sh_name)
    names.append(df.columns[0])
    if sh_name == 'Season A':
        crops = df.columns[1:-1]

# Create a Dash app instance
app = Dash(__name__)

# Remove duplicates from the lists
years = list(set(years))
indicators = list(set(indicators))
names = list(set(names))

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
    html.H1(children='SEASONAL AGRICULTURAL SURVEY (SAS)', style={'textAlign':'center'}),
    html.H3(children='EXECUTIVE SUMMARY', style={'textAlign':'center'}),
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
        value=indicators[0]
    ),
    dcc.Graph(figure={}, id='bar-chart-1'),
    html.Label('Choose year:'),
    dcc.RadioItems(options=[2021, 2022], value=2021, inline=True, id='years-dropdown'),
    html.Label('Choose the data of your interest:'),
    dcc.Dropdown(
        id='names',
        options=[{'label': name, 'value': name} for name in names],
        value=names[0]
    ),
    html.Label('Choose the crop of your interest:'),
    dcc.Dropdown(
        id='crops',
        options=[{'label': crop, 'value': crop} for crop in crops],
        value=crops[0]
    ),
    dcc.Graph(figure={}, id='pie-charts-1'),
    dcc.Graph(figure={}, id='pie-charts-2')
])

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
    season_A = go.Bar(x=df[df.columns[0]], y=df[df.columns[1]], name=df.columns[1])
    season_B = go.Bar(x=df[df.columns[0]], y=df[df.columns[2]], name=df.columns[2])
    season_C = go.Bar(x=df[df.columns[0]], y=df[df.columns[3]], name=df.columns[3])

    # Add the traces to the subplots
    figure.add_trace(season_A, row=1, col=1)
    figure.add_trace(season_B, row=1, col=1)
    figure.add_trace(season_C, row=1, col=1)

    df2 = other_file.parse('Sheet1')
    figure2 = go.Bar(x=df2[df2.columns[0]], y=df2[df2.columns[1]])
    
    figure.add_trace(figure2, row=1, col=2)
    figure.update_layout(
        title_text=f'{chosen_year} - {chosen_indicator} in Seasons A, B, and C'
    )
    return figure

@app.callback(
    Output('pie-charts-1', 'figure'),
    [Input('years-dropdown', 'value'), Input('names', 'value')]
)
def pie_updater_one(year, name):
    fig_pie = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]], subplot_titles=("Season A", "Season B", "Season C"))
    for sheet in sheets[1:]:
        pie_df = other_file.parse(sheet)
        if pie_df.columns[0] == name and year == pie_df.columns[4]:
            fig_pie.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[pie_df.columns[1]].tolist()), 1, 1)
            fig_pie.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[pie_df.columns[2]].tolist()), 1, 2)
            fig_pie.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[pie_df.columns[3]].tolist()), 1, 3)
            break
    if fig_pie:
        fig_pie.update_layout(title_text=name)
        fig_pie.update_traces(textposition='inside')
    return fig_pie

@app.callback(
    Output('pie-charts-2', 'figure'),
    [Input('years-dropdown', 'value'), Input('names', 'value'), Input('crops', 'value')]
)
def pie_updater_two(year, name, crop):
    fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]], subplot_titles=("Season A", "Season B", "Season C"))
    for sheet in sheets[1:]:
        pie_df = other_file.parse(sheet)
        if year == 2022 and pie_df.columns[0] == name and crop != None:
            if sheet == 'Season A':
                fig.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[crop].tolist()), 1, 1)
            elif sheet == 'Season B' and year in pie_df.columns:
                fig.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[crop].tolist()), 1, 2)
            elif sheet == 'Season C' and year in pie_df.columns:
                fig.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[crop].tolist()), 1, 3)
    if year == 2022 and pie_df.columns[0] == name:
        fig.update_layout(title_text=crop)
        fig.update_traces(textposition='inside')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)