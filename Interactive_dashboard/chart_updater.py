from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import filter

def bar_chart(app, summary_file):
    @app.callback(
        Output('bar-chart-1', 'figure'),
        [Input('year-dropdown', 'value'), Input('indicator-dropdown', 'value')]
        )
    
    def chart_updater(chosen_year, chosen_indicator):
        figure = go.Figure()
        for sheet in summary_file.sheet_names:
            df = summary_file.parse(sheet)
            if df.columns[0] == chosen_indicator and df.columns[4] == chosen_year:
                break

        figure.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[1]], name=df.columns[1]))
        figure.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[2]], name=df.columns[2]))
        figure.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[3]], name=df.columns[3]))

        figure.update_layout(
            title_text=f'{chosen_year} - {chosen_indicator} in seasons A, B, and C', xaxis=dict(showgrid=True), font=dict(family='Cambria, "Times New Roman", serif', size=16)
            )
        figure.update_xaxes(title_text=filter.filter_X_axis(chosen_indicator))
        figure.update_yaxes(title_text=filter.filter_Y_axis(chosen_indicator))

        return figure
