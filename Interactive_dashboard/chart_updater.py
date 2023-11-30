from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import filter

def bar_chart(app, summary_file, other_file):
    @app.callback(
        Output('bar-chart-1', 'figure'),
        [Input('year-dropdown', 'value'), Input('indicator-dropdown', 'value')]
        )
    
    def chart_updater(chosen_year, chosen_indicator):
        figure = make_subplots(rows=1, cols=3, specs=[[{'type': 'xy'}, {'type': 'xy'}, {'type': 'xy'}]], subplot_titles=("Season A", "Season B", "Season C"), horizontal_spacing=0.1)
        for sheet in summary_file.sheet_names:
            df = summary_file.parse(sheet)
            if df.columns[0] == chosen_indicator and df.columns[4] == chosen_year:
                break
            
        # Create a bar chart with multiple y-values on first column
        figure.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[1]], name=df.columns[1]), row=1, col=1)
        figure.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[2]], name=df.columns[2]), row=1, col=2)
        figure.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[3]], name=df.columns[3]), row=1, col=3)

        # create the second chart on second column  
        # df2 = other_file.parse('Sheet1')
        # df2 = df2.sort_values(by=df2.columns[1])
        # figure.add_trace(go.Bar(x=df2[df2.columns[0]], y=df2[df2.columns[1]]), row=1, col=2)
        figure.update_layout(
            title_text=f'{chosen_year} - {chosen_indicator} in seasons A, B, and C', font=dict(family='Cambria, "Times New Roman", serif', size=16)
            )
        figure.update_xaxes(title_text=filter.filter_X_axis(chosen_indicator), row=1, col=1)
        figure.update_yaxes(title_text=filter.filter_Y_axis(chosen_indicator), row=1, col=1)
        figure.update_xaxes(title_text=filter.filter_X_axis(chosen_indicator), row=1, col=2)
        figure.update_yaxes(title_text=filter.filter_Y_axis(chosen_indicator), row=1, col=2)
        figure.update_xaxes(title_text=filter.filter_X_axis(chosen_indicator), row=1, col=3)
        figure.update_yaxes(title_text=filter.filter_Y_axis(chosen_indicator), row=1, col=3)
        # figure.update_xaxes(title_text='Land class', row=1, col=2)
        # figure.update_yaxes(title_text='Area in hectares', row=1, col=2)
        return figure
