from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import filter
import numpy as np

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
        figure1, figure2, figure3 = None, None, None
        for sheet in detailed_file.sheet_names:
            detailed_f = detailed_file.parse(sheet)
            if detailed_f.columns[0] == detailed_indicator and 'Season A' in detailed_f.columns:
                detailed_f['Density'] = pd.to_numeric(detailed_f[indicator], errors='coerce').apply(lambda x: np.log10(x if not np.isnan(x) and x != 0 else 1))
                detailed_f['id'] = detailed_f[detailed_f.columns[0]].apply(lambda x: district_id_map.get(x, None))
                detailed_f = detailed_f.rename(columns={detailed_f.columns[0]: 'District'})
                figure1 = px.choropleth_mapbox(detailed_f, geojson=Rwanda_districts, locations='id', color='Density', hover_data=['Density', indicator, detailed_f.columns[0]],
                                               mapbox_style="carto-positron", center={"lat": -1.9403, "lon": 29.8739}, zoom=7)
                figure1.update_layout(title=f'{indicator} in Season A', font=dict(family='Cambria, "Times New Roman", serif', size=16))
            elif detailed_f.columns[0] == detailed_indicator and 'Season B' in detailed_f.columns:
                detailed_f['Density'] = pd.to_numeric(detailed_f[indicator], errors='coerce').apply(lambda x: np.log10(x if not np.isnan(x) and x != 0 else 1))
                detailed_f['id'] = detailed_f[detailed_f.columns[0]].apply(lambda x: district_id_map.get(x, None))
                detailed_f = detailed_f.rename(columns={detailed_f.columns[0]: 'District'})
                figure2 = px.choropleth_mapbox(detailed_f, geojson=Rwanda_districts, locations='id', color='Density', hover_data=['Density', indicator, detailed_f.columns[0]],
                                               mapbox_style="carto-positron", center={"lat": -1.9403, "lon": 29.8739}, zoom=7)
                figure2.update_layout(title=f'{indicator} in Season B', font=dict(family='Cambria, "Times New Roman", serif', size=16))
            elif detailed_f.columns[0] == detailed_indicator and 'Season C' in detailed_f.columns:
                detailed_f['Density'] = pd.to_numeric(detailed_f[indicator], errors='coerce').apply(lambda x: np.log10(x if not np.isnan(x) and x != 0 else 1))
                detailed_f['id'] = detailed_f[detailed_f.columns[0]].apply(lambda x: district_id_map.get(x, None))
                detailed_f = detailed_f.rename(columns={detailed_f.columns[0]: 'District'})
                figure3 = px.choropleth_mapbox(detailed_f, geojson=Rwanda_districts, locations='id', color='Density', hover_data=['Density', indicator, detailed_f.columns[0]],
                                               mapbox_style="carto-positron", center={"lat": -1.9403, "lon": 29.8739}, zoom=7)
                figure3.update_layout(title=f'{indicator} in Season C', font=dict(family='Cambria, "Times New Roman", serif', size=16))
                break
        return figure1, figure2, figure3