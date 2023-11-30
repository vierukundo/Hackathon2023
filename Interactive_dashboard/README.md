# Seasonal Agricultural Survey (SAS) Dashboard

This Dash web application provides visualizations and insights derived from the Seasonal Agricultural Survey (SAS) conducted in Rwanda. The SAS collects vital agricultural information, contributing to the monitoring of national programs and informed decision-making. The application utilizes the Dash framework for creating interactive and visually appealing dashboards.

# Getting Started

# Prerequisites and Installation

Make sure you have the required Python libraries installed. You can install them using the following:

pip install dash pandas plotly openpyxl numpy

Note: This app uses dash version 2.14 or later.

If you're using Dash version 2.13 or earlier, you need to include __name__ in your Dash constructor when running in order to render on the css files on app layout.

# Running the Application

Clone or download the repository to your local machine.

git clone https://github.com/vierukundo/Hackathon2023.git

# Navigate to the project directory.

cd Hackathon2023/Interactive_dashboard

# Run the Dash application script by running this command.

python app.py

Open your web browser and go to http://127.0.0.1:8050/ to view the SAS Dashboard.

# Dashboard Sections

# Executive Summary

The dashboard begins with an executive summary, providing context and highlights related to the SAS findings for the agricultural year 2021/2022. It covers key agricultural seasons (Season A, Season B, and Season C) and highlights main indicators, including:

Land use
Crop land
Crop production
Crop yield
Use of inputs
Agricultural practices

# Main Indicators Bar Chart

The bar chart illustrates the summary of Seasonal Agricultural Survey main indicators for the last three years. Use the dropdowns to choose the year and indicator of interest.

# Other Findings Pie Charts

This section presents pie charts depicting findings from other aspects of the SAS. Users can choose the year and explore data related to specific items.

# Detailed Agricultural Analysis Maps

The last section provides detailed choropleth maps for each agricultural season (Season A, Season B, and Season C) based on user-selected indicators. The maps visualize the density of the chosen indicator in each district of Rwanda.


# Acknowledgments
This SAS Dashboard is developed using the Dash framework and leverages Plotly for data visualization. Special thanks to the National Institute of Statistics of Rwanda for providing the data used in this dashboard.
