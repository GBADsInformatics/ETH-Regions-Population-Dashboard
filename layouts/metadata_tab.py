import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
from dash import dash_table
from layouts.layout import CONTENT_STYLE_TABLES
from layouts import layout
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


metadata_content = dbc.Row(
    [
        dbc.Col(layout.sidebar_metadata, 
                xs=dict(order=1, size=12),
                sm=dict(order=1, size=3)
                ),
        dbc.Col(table,
                xs=dict(order=2, size=12),
                sm=dict(order=2, size='auto'))
    ], className='root-container'
)