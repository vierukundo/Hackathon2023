import json
# filter the content of X-axis and Y-axis

indicator_units = {
    "Share of pure crop in agricultural land": "Percentage (%)", "Agricultural inputs": "Percentage (%)",
    "Agricultural practices": "Percentage (%)", "Agricultural area": "Hectares (,000Ha)",
    "Yield for major crops (Kg/ha)": "Kilograms per hectare (Kg/Ha)", "Production for major crops (MT)": "Metric tones (MT)",
    "Harvested area for major crops (Ha)": "Hectares (Ha)", "Cultivated area for major crops (Ha)": "Hectares (Ha)"
}

indicator_labels = {
    "Share of pure crop in agricultural land": "Farmers category", "Agricultural inputs": "Agricultural inputs",
    "Agricultural practices": "Farmers", "Agricultural area": "Agricultural area",
    "Yield for major crops (Kg/ha)": "Major crops", "Production for major crops (MT)": "Major crops",
    "Harvested area for major crops (Ha)": "Major crops", "Cultivated area for major crops (Ha)": "Major crops"
}

def filter_Y_axis(indicator):
    if indicator in indicator_units.keys():
        return indicator_units[indicator]
    else:
        return None

def filter_X_axis(indicator):
    if indicator in indicator_labels.keys():
        return indicator_labels[indicator]
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
        district_id_map[feature['properties']['NAME_2']] = feature['id']  # Convert to string
    return [Rwanda_districts, district_id_map]