import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
from dash import dash_table
from layouts.styling import SIDEBAR_STYLE, CONTENT_STYLE_TABLES
import pandas as pd

def get_metadata_df(choice): 

    if choice == 'csa': 
        return(m_csa)
    elif choice == 'cattle':
        return(m_cattle)
    elif choice == 'camels':
        return(m_camels)
    elif choice == 'poultry':
        return(m_poultry)
    
###--------------Read in metadata-----------------------------------
m_csa = pd.read_csv('data/m_csa.csv')
m_cattle = pd.read_csv('data/m_cattle.csv')
m_camels = pd.read_csv('data/m_camels.csv')
m_poultry = pd.read_csv('data/m_poultry.csv')

table = html.Div([
    html.P("Select a dataset on the left sidebar to view the metadata."),
    dash_table.DataTable(
            id='metadata-table',
            export_format='csv',
            style_cell={'textAlign': 'left', 'font-family':'sans-serif'},
            style_table={'height': '600px', 'overflowY': 'auto'},
            style_data={
                'color': 'black',
            }
)])

sidebar_metadata = html.Div(
    [
        html.H4("Options"),
        html.Hr(),
        dbc.Nav(
            [  
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset',value ='csa', persistence=True, persistence_type='session'),
                html.H6(" ")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id = "sidebar-metadata",
    style=SIDEBAR_STYLE,
)

metadata_content = dbc.Row(
            [
            sidebar_metadata,
            dbc.Col(table, style = CONTENT_STYLE_TABLES)
            ]
)
