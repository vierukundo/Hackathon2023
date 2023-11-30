from dash.dependencies import Input, Output
import plotly.express as px
import filter

seasons = ['Season A', 'Season B', 'Season C']

def map_updater(app, detailed_file):
    @app.callback(
        [Output('chosen_detailed_indicator', 'options'), Output('chosen_detailed_indicator', 'value')],
        Input('detailed_indicator', 'value')
        )
    # this updates the dropdown with dataset of selected indicator
    def update_drop_down(detailed_indicator):
        for sheet in detailed_file.sheet_names:
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
        Rwanda_districts = filter.filter_map()[0]
        district_id_map = filter.filter_map()[1]
        unit = filter.get_units(detailed_indicator)
        figures = []
        for sheet in detailed_file.sheet_names:
            detailed_f = detailed_file.parse(sheet)
            if detailed_f.columns[0] == detailed_indicator and detailed_f.columns[-1] in seasons:
                detailed_f['id'] = detailed_f[detailed_f.columns[0]].apply(lambda x: district_id_map.get(x, None))
                figure = px.choropleth_mapbox(detailed_f, geojson=Rwanda_districts, locations='id', color=indicator, hover_data=[indicator, detailed_f.columns[0]], labels={detailed_f.columns[0]: "District", indicator:unit},
                                               mapbox_style="carto-positron", center={"lat": -1.9403, "lon": 29.8739}, zoom=7)
                figure.update_layout(title=f'{indicator} in {detailed_f.columns[-3]}', font=dict(family='Cambria, "Times New Roman", serif', size=16))
                figures.append(figure)
                if len(figures) == 3:
                    break

        return figures