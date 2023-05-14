import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash_bootstrap_templates import load_figure_template
from dash import dash_table
from layouts import styling 
import requests
import json
import pandas as pd

# Potentially switch this to leaflet https://dash-leaflet.herokuapp.com/

my_color_scale = [[0.0, '#4c5c73'], [0.1, '#5D6C81'], [0.2, '#6F7C8F'], [0.3, '#818C9D'], [0.4, '#939DAB'],
                  [0.5, '#A5ADB9'], [0.6, '#B7BDC7'], [0.7, '#C9CED5'], [0.8, '#DBDEE3'], [0.9, '#EDEEF1'],
                  [1.0, '#FFFFFF']]

def create_map(merged_df, dataset, species, year):

    yr = year
    sp = species

# Ethiopia geojson files from S3
# Regional level
#    url = 'https://gbads-data-repo.s3.ca-central-1.amazonaws.com/shape-files/eth_admbnda_adm1_csa_bofedb_2021.geojson'
#    r = requests.get(url, allow_redirects=True)
#    geojson_eth = r.json()

# Ethiopia geojson files from file in ../assets
# Regional level
    with open('assets/eth_admbnda_adm1_csa_bofedb_2021.geojson') as file:
        geojson_eth = json.load(file)

    if dataset == "csa":
        newdf = pd.read_csv('data/csa.csv')
    elif dataset == "cattle":
        newdf = pd.read_csv('data/cattle.csv')
    elif dataset == "camels":
        newdf = pd.read_csv('data/camels.csv')


# get all 'yr' numbers for 'sp'
    filter1 = newdf.query(f'year == {yr}')
    filtered = filter1.query(f'species == "{sp}"')
    pops = filtered['population'].tolist()
    enCode = ['Addis Ababa', 'Afar', 'Amhara', 'Benishangul Gumz', 'Dire Dawa', 'Gambela', 'Harari', 'Oromoa', 'SNNPR', 'Somali', 'Tigray' ]
    filtered.region = filtered.region.map({ 'Addis Ababa' : 'ET14', 'Afar' : 'ET02', 'Amhara' : 'ET03', 'Benishangul Gumz' : 'ET06', 'Dire Dawa' : 'ET15', 'Gambela' : 'ET12', 'Harari' : 'ET13', 'Oromoa' : 'ET04', 'SNNPR' : 'ET07', 'Somali' : 'ET05', 'Tigray' : 'ET01', 'SI' : 'ET16', 'SW' : 'ET11' })
    filtered.insert(2, "AdminEN", enCode, True)
    max_val = max(pops)

# Set location based on the granularity level of data - currently Region
    featureid = 'ADM1_PCODE'
    location = 'region'

# Set the featureid key needed for the chrorpleth mapbox map
    featurekey = (f'properties.{featureid}')

    fig = px.choropleth_mapbox(filtered,
       geojson=geojson_eth,
       locations=location,
       featureidkey=featurekey,
       hover_data={'region': False, 'AdminEN':True, 'population':True},
       color='population',
       color_continuous_scale='sunset',
       opacity=0.7,
       mapbox_style="white-bg",
       zoom=4.5,
       center = {"lat": 9.1450, "lon": 40.4897},
       labels={'region': 'Region'}
       )

# Adjust margins
    fig.update_layout(
        margin=dict(l=5, r=10, b=8),
    )

    fig.update_geos(showsubunits=True, subunitcolor='Black', showcountries=True, showcoastlines=False, showland=False, fitbounds="locations")
# Add title
    fig.update_layout(
        title_text=f'{sp.capitalize()} Population in {yr}',
    font_size=15
)

# Update legend title   
    fig.update_layout(
        coloraxis_colorbar=dict(
        title="Head",
        )
    )
    fig.update_layout(
        legend=dict(orientation="h")
    )

    return(fig)

map = dcc.Graph(id = 'map', config = styling.plot_config)

content = dbc.Row(children=
            [
            styling.sidebar_map,
            dcc.Loading(id = "loading-icon", 
                children=[
                dbc.Col(map)])
            ], style = styling.CONTENT_STYLE_GRAPHS
        )
