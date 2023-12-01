import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
from dash import dash_table
from layouts import layout

table = html.Div([
    html.P("Use the selections in the OPTIONS side bar on the left to filter the data and the export button to download the data in csv format."),
    dash_table.DataTable(
            id='datatable',
            export_format='csv',
            style_cell={'textAlign': 'left', 'font-family':'sans-serif'},
            style_table={'height': '600px', 'overflowY': 'auto'},
            style_data={
                'color': 'black',
            },
            style_header={
                'color': 'black',
                'fontWeight': 'bold'
            }
)])

content = dbc.Row(
    [
        dbc.Col(layout.sidebar_download, 
                xs=dict(order=1, size=12),
                sm=dict(order=1, size=3)
                ),
        dbc.Col(table,
                xs=dict(order=2, size=12),
                sm=dict(order=2, size='auto'))
    ], className='root-container'
)