import json

y_axis = {
    "Share of pure crop in agricultural land": "Percentage (%)", "Agricultural inputs": "Percentage (%)",
    "Agricultural practices": "Percentage (%)", "Agricultural area": "Hectares (,000Ha)",
    "Yield for major crops (Kg/ha)": "Kilograms per hectare (Kg/Ha)", "Production for major crops (MT)": "Metric tones (MT)",
    "Harvested area for major crops (Ha)": "Hectares (Ha)", "Cultivated area for major crops (Ha)": "Hectares (Ha)"
}

x_axis = {
    "Share of pure crop in agricultural land": "Farmers category", "Agricultural inputs": "Agricultural inputs",
    "Agricultural practices": "Farmers", "Agricultural area": "Agricultural area",
    "Yield for major crops (Kg/ha)": "Major crops", "Production for major crops (MT)": "Major crops",
    "Harvested area for major crops (Ha)": "Major crops", "Cultivated area for major crops (Ha)": "Major crops",
    "Percentage of farmers by source of inorganic fertilizers": "Source of inorganic fertilizers", "Source of improved seeds (%)": "Source of improved seeds",
    "Use of production by farmers and per crop type (%)": "Use of production", "Source of inorganic fertiliser by type of fertilizer (%)": "Source of inorganic fertiliser",
    "Source of improved seeds by season per crop type in 2022 (%)": "Source of improved seeds"
}

# filter the content of Y-axis
def filter_Y_axis(indicator):
    if indicator in y_axis.keys():
        return y_axis[indicator]
    else:
        return None

# filter the content of X-axis
def filter_X_axis(indicator):
    if indicator in x_axis.keys():
        return x_axis[indicator]
    else:
        return None

def filter_indicators(file):
    indicators = []
    for sheet in file.sheet_names:
        df = file.parse(sheet)
        if df.columns[0] not in indicators:
            indicators.append(df.columns[0])
    return indicators

def filter_map():
    # read the Rwanda geojson file
    with open('rwanda_geojson.geojson', 'r') as f:
        Rwanda_districts = json.load(f)
        
    district_id_map = {}
    for feature in Rwanda_districts['features']:
        feature['id'] = str(feature['properties']['ID_2'])
        district_id_map[feature['properties']['NAME_2']] = feature['id'] # store districts names and respective IDs
    return [Rwanda_districts, district_id_map]