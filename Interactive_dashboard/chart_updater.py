from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import filter

def bar_chart(app, summary_file, districts_level_file):
    @app.callback(
        Output('bar-chart-1', 'figure'),
        [Input('year-dropdown', 'value'), Input('indicator-dropdown', 'value')]
        )
    
    def chart_updater(chosen_year, chosen_indicator):
        figure = make_subplots(rows=1, cols=2, specs=[[{'type': 'xy'}, {'type': 'xy'}]], subplot_titles=(f'{chosen_indicator}', "Rwanda Land cover classes"))
        for sheet in summary_file.sheet_names:
            df = summary_file.parse(sheet)
            if df.columns[0] == chosen_indicator and df.columns[4] == chosen_year:
                break
            
        # Create a bar chart with multiple y-values
        figure.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[1]], name=df.columns[1]), row=1, col=1)
        figure.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[2]], name=df.columns[2]), row=1, col=1)
        figure.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[3]], name=df.columns[3]), row=1, col=1)
            
        df2 = districts_level_file.parse('Sheet1')
        figure2 = go.Bar(x=df2[df2.columns[0]], y=df2[df2.columns[1]])
        figure.add_trace(figure2, row=1, col=2)
        figure.update_layout(
            title_text=f'{chosen_year} - {chosen_indicator} in seasons A, B, and C', font=dict(family='Cambria, "Times New Roman", serif', size=16)
            )
        figure.update_xaxes(title_text=filter.filter_X_axis(chosen_indicator), row=1, col=1)
        figure.update_yaxes(title_text=filter.filter_Y_axis(chosen_indicator), row=1, col=1)
        figure.update_xaxes(title_text='Land class', row=1, col=2)
        figure.update_yaxes(title_text='Area in hectares', row=1, col=2)
        return figure
