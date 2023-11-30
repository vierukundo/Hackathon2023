from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from filter import filter_X_axis

seasons = ['Season A', 'Season B', 'Season C']

def pie_chart_updater(app, other_file):
    @app.callback(
        [Output('names', 'options'), Output('names', 'value')],
        Input('years-dropdown', 'value')
        )
    
    # this updates the dropdown based on the selected year of survey
    def check_year(year):
        names = []
        if year == 2021:
            new_sheets = other_file.sheet_names[1:13]
        else:
            new_sheets = other_file.sheet_names
        for sh_name in new_sheets:
            df = other_file.parse(sh_name)
            if df.columns[0] not in names:
                names.append(df.columns[0])
                options = [{'label': name, 'value': name} for name in names]
        return options, names[0]
    
    @app.callback(
        [Output('data', 'options'), Output('data', 'value')],
        [Input('years-dropdown', 'value'), Input('names', 'value')]
        )
    def update_data(year, name):
        for sheet in other_file.sheet_names:
            pie_df = other_file.parse(sheet)
            if pie_df.columns[0] == name and year == pie_df.columns[-1]:
                break
        return pie_df.columns[1:-2], pie_df.columns[1]
    # This updates the piecharts according to year and dataset selected
    @app.callback(
        Output('pie-charts-1', 'figure'),
        [Input('years-dropdown', 'value'), Input('names', 'value'), Input('data', 'value')]
        )
    def pie_updater_one(year, name, data):
        fig_pie = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]], subplot_titles=("Season A", "Season B", "Season C"), horizontal_spacing=0.1)
        fig_line = make_subplots(rows=1, cols=3, specs=[[{'type':'xy'}, {'type':'xy'}, {'type':'xy'}]], subplot_titles=("Season A", "Season B", "Season C"), horizontal_spacing=0.1)
        
        for sheet in other_file.sheet_names:
            pie_df = other_file.parse(sheet)
            if pie_df.columns[0] == name and year in pie_df.columns:
                season = None
                
                if 'Season A' in pie_df.columns:
                    season = 'Season A'
                elif 'Season B' in pie_df.columns:
                    season = 'Season B'
                elif 'Season C' in pie_df.columns:
                    season = 'Season C'
                if season and len(pie_df.columns) < 7:
                    fig_pie.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[data].tolist()), 1, 1 + seasons.index(season))
                elif season and len(pie_df.columns) >= 7:
                    fig_line.add_trace(go.Scatter(x=pie_df[pie_df.columns[0]], y=pie_df[data], mode='lines+markers', name='markers'), 1, 1 + seasons.index(season))
                else:
                    fig_line = make_subplots(rows=1, cols=2, specs=[[{'type':'xy'}, {'type':'xy'}]], subplot_titles=("Area", "Percentage (%)"), horizontal_spacing=0.1)
                    fig_line.add_trace(go.Scatter(x=pie_df[pie_df.columns[0]], y=pie_df[pie_df.columns[1]], mode='lines+markers', name='markers'), 1, 1)
                    fig_line.add_trace(go.Scatter(x=pie_df[pie_df.columns[0]], y=pie_df[pie_df.columns[2]], mode='lines+markers', name='markers'), 1, 2)
                    break
            if len(fig_pie['data']) == 3 or len(fig_line['data']) == 3:
                break
        if len(fig_pie['data']) == 3:
            fig_pie.update_traces(textposition='inside')
        elif len(fig_line['data']) == 3: 
            for i in range(3):
                fig_line.update_xaxes(title_text=filter_X_axis(name), row=1, col= i + 1)
                fig_line.update_yaxes(title_text="Percentage (%)", row=1, col= i + 1, range=[0, 100])
        else:
            fig_line.update_xaxes(title_text="Land class", row=1, col=1)
            fig_line.update_yaxes(title_text="Area in hectares", row=1, col=1)
            fig_line.update_xaxes(title_text="Land class", row=1, col=2)
            fig_line.update_yaxes(title_text="Area in (%)", row=1, col=2, range=[0, 100])
        fig = fig_pie if len(fig_pie['data']) == 3 else fig_line
        fig.update_layout(title_text=name, font=dict(family='Cambria, "Times New Roman", serif', size=16), height=450)

        return fig
