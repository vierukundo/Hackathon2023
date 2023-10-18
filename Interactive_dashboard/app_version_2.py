from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Read the Excel file and get sheet names
excel_file = pd.ExcelFile('Summary of SAS.xlsx')
sheet_names = excel_file.sheet_names

# Initialize lists for indicators and years
indicators = []
years = []

# Iterate through the sheets to gather indicator and year data
for sheet_name in sheet_names:
    df = excel_file.parse(sheet_name)
    indicators.append(df.columns[0])
    years.append(df.columns[4])

# Create a Dash app instance
app = Dash(__name__)

# Remove duplicates from the lists
years = list(set(years))
indicators = list(set(indicators))

# Define the layout of the web application
app.layout = html.Div([
    html.Div(children='Summary of Seasonal Agricultural Survey'),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in years],
        value=years[0]
    ),
    dcc.Dropdown(
        id='indicator-dropdown',
        options=[{'label': indicator, 'value': indicator} for indicator in indicators],
        value=indicators[0]
    ),
    dcc.Graph(figure={}, id='bar-chart-1')
])

@app.callback(
    Output('bar-chart-1', 'figure'),
    [Input('year-dropdown', 'value'), Input('indicator-dropdown', 'value')]
)
def chart_updater(chosen_year, chosen_indicator):
    for sheet_name in sheet_names:
        df = excel_file.parse(sheet_name)
        if df.columns[0] == chosen_indicator and df.columns[4] == chosen_year:
            break

    # Create a bar chart with multiple y-values
    figure1 = px.bar(df, x=df.columns[0], y=[df.columns[1], df.columns[2], df.columns[3]], 
                     labels={df.columns[0]: 'Major Crops', 
                             df.columns[1]: 'Cultivated area in Season A', 
                             df.columns[2]: 'Cultivated area in Season B', 
                             df.columns[3]: 'Cultivated area in Season C'},
                     title=f'{chosen_year} - {chosen_indicator} in Seasons A, B, and C')

    return figure1

if __name__ == '__main__':
    app.run_server(debug=True)