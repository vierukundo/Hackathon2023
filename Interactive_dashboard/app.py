from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

excel_file = pd.ExcelFile('Summary of SAS.xlsx')
sheet_names = excel_file.sheet_names
indicators = []
years = []

for sheet_name in sheet_names:
    df = excel_file.parse(sheet_name)
    indicators.append(df.columns[0])
    years.append(df.columns[4])

app = Dash(__name__)
years = list(set(years)) # remove duplicates
indicators = list(set(indicators))


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
    dcc.Graph(figure={}, id='bar-chart-1'),
    dcc.Graph(figure={}, id='bar-chart-2'),
    dcc.Graph(figure={}, id='bar-chart-3')
])

@app.callback(
    [Output('bar-chart-1', 'figure'), Output('bar-chart-2', 'figure'), Output('bar-chart-3', 'figure')],
    [Input('year-dropdown', 'value'), Input('indicator-dropdown', 'value')]
)
def chart_updater(chosen_year, chosen_indicator):
    for sheet_name in sheet_names:
        df = excel_file.parse(sheet_name)
        if df.columns[0] == chosen_indicator and df.columns[4] == chosen_year:
            break
    figure1 = px.bar(df, x=df.columns[0], y=df.columns[1], title=f'{chosen_year} - {chosen_indicator} in Season A')
    figure2 = px.bar(df, x=df.columns[0], y=df.columns[2], title=f'{chosen_year} - {chosen_indicator} in Season B')
    figure3 = px.bar(df, x=df.columns[0], y=df.columns[3], title=f'{chosen_year} - {chosen_indicator} in Season c')
    return figure1, figure2, figure3

if __name__ == '__main__':
    app.run_server(debug=True)