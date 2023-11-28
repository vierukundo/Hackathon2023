from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def pie_chart_updater(app, districts_level_file):
    @app.callback(
        [Output('names', 'options'), Output('names', 'value')],
        Input('years-dropdown', 'value')
        )
    
    # this updates the dropdown based on the selected year of survey
    def check_year(year):
        names = []
        if year == 2021:
            new_sheets = districts_level_file.sheet_names[1:13]
        else:
            new_sheets = districts_level_file.sheet_names[1:]
        for sh_name in new_sheets:
            df = districts_level_file.parse(sh_name)
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
        for sheet in districts_level_file.sheet_names[1:]:
            pie_df = districts_level_file.parse(sheet)
            if pie_df.columns[0] == name and year in pie_df.columns and 'Season A' in pie_df.columns:
                fig_pie.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[pie_df.columns[1]].tolist()), 1, 1)
            elif pie_df.columns[0] == name and year in pie_df.columns and 'Season B' in pie_df.columns:
                fig_pie.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[pie_df.columns[1]].tolist()), 1, 2)
            elif pie_df.columns[0] == name and year in pie_df.columns and 'Season C' in pie_df.columns:
                fig_pie.add_trace(go.Pie(labels=pie_df[pie_df.columns[0]].tolist(), values=pie_df[pie_df.columns[1]].tolist()), 1, 3)
                break
        
        if fig_pie:
            fig_pie.update_layout(title_text=name, font=dict(family='Cambria, "Times New Roman", serif', size=16))
            fig_pie.update_traces(textposition='inside')
            
        return fig_pie
