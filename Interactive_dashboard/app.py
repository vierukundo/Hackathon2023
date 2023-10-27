from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go

excel_file = pd.ExcelFile('Summary of SAS.xlsx')
sheet_names = excel_file.sheet_names
other_file = pd.ExcelFile('other_findings.xlsx')
sheets = other_file.sheet_names
indicators = []
years = []

for sheet_name in sheet_names:
    df = excel_file.parse(sheet_name)
    indicators.append(df.columns[0])
    years.append(df.columns[4])

names = []
crops = []
for sh_name in sheets:
    df = other_file.parse(sh_name)
    names.append(df.columns[0])
    if sh_name == 'Season A':
        crops = df.columns[1:-1]

app = Dash(__name__)
years = list(set(years))  # remove duplicates
indicators = list(set(indicators))
names = list(set(names))

# Create subplots



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
    dcc.Graph(figure={}, id='bar-chart-3'),

    dcc.Dropdown(
        id='years-dropdown',
        options=[{'label': 2021, 'value': 2021}, {'label': 2022, 'value': 2022}],
        value=2021
    ),
    dcc.Dropdown(
        id='names',
        options=[{'label': name, 'value': name} for name in names],
        value=names[0]
    ),
    dcc.Dropdown(
        id='crops',
        options=[{'label': crop, 'value': crop} for crop in crops],
        value=crops[0]
    ),
    dcc.Graph(figure={}, id='pie-charts-1'),
    dcc.Graph(figure={}, id='pie-charts-2')
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
    figure3 = px.bar(df, x=df.columns[0], y=df.columns[3], title=f'{chosen_year} - {chosen_indicator} in Season C')
    return figure1, figure2, figure3

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
