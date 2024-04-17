import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash_bootstrap_templates import load_figure_template
from app import app
from os import environ as env

load_figure_template('LUX')

GBADSLOGOB = env.get('BASE_URL','') + "/assets/GBADsLogo.png"

ACTIVE_TAB_STYLE = {
    "color": "#FFA500"
}

CONTENT_STYLE = {
    "top":"8rem",
    "margin-left": "25rem",
    "margin-right": "8rem",
    "bottom": "2rem",
    "padding": "7rem 2rem 2rem",
    "overflow": "scroll"
}

CONTENT_STYLE_TABLES = {
    "top":"8rem",
    "margin-left": "20rem",
    "margin-right": "7rem",
    "bottom": "2rem",
    "padding": "5rem 2rem 2rem",
    "overflow": "scroll",
    "position": "fixed"
}

CONTENT_STYLE_GRAPHS = {
    "top":"8rem",
    "margin-left": "20rem",
    "margin-right": "7rem",
    "bottom": "2rem",
    "padding": "5rem 2rem 2rem",
    "position": "fixed"
}


MAP_STYLE = {
    "top":"8rem",
    "margin-left": "20rem",
    "margin-right": "7rem",
    "bottom": "2rem",
    "padding": "7rem 2rem 2rem",
    "overflow": "scroll",
}

plot_config = {'displayModeBar': True,
          'displaylogo': False}

sidebar_metadata = html.Div(
    [
        dbc.Row(
            [
                html.H4('Options', className="sidebar"),
            ],
            style={"height": "5vh"}
            ),
        dbc.Row(
            [  
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset',value ='csa', persistence=True, persistence_type='session'),
                html.H6(" ")
            ], className = "sidebar"
        ),
    ],
    id = "sidebar-metadata"
)

sidebar_download = html.Div(
    [
        dbc.Row(
            [
                html.H4('Options', className="sidebar"),
            ],
            style={"height": "5vh"}
            ),
        dbc.Row(
            [  
                html.H6("Select multiple:", id='choice-title'),
                dcc.RadioItems(
                ['Species', 'Regions'], 'Species', inline=True, id='choice', persistence_type='session', persistence=True
                ),
                html.H6(" "),
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset', value = 'csa', persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Region:"),
                dcc.Dropdown(id = 'region', value = 'Afar', persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Species:"),
                dcc.Dropdown(id = 'species', value = ['cattle','sheep'], persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Start year:"),
                dcc.Dropdown(id = 'start year', value = 2003, persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("End year:"),
                dcc.Dropdown(id = 'end year',value = 2020, persistence_type='session', persistence=True)
            ], className="sidebar"
        )
    ]
)


sidebar = html.Div(
    [
        dbc.Row(
            [
            html.H4("Options"),
            html.H6("Select multiple:", id='choice-title'),
            dcc.RadioItems(
            ['Species', 'Regions'], 'Species', inline=True, id='choice', persistence_type='session', persistence=True),
            html.H6(" "),
            html.H6("Dataset:"),
            dcc.Dropdown(id = 'dataset', value='csa', persistence_type='session', persistence=True),
            html.H6(" "),
            html.H6("Region:"),
            dcc.Dropdown(id = 'region', value = 'Afar', persistence_type='session', persistence=True),
            html.H6(" "),
            html.H6("Species:"),
            dcc.Dropdown(id = 'species', value = ['cattle','sheep'],persistence_type='session', persistence=True),
            html.H6(" "),
            html.H6("Start year:"),
            dcc.Dropdown(id = 'start year', value = 2003, persistence_type='session', persistence=True),
            html.H6(" "),
            html.H6("End year:"),
            dcc.Dropdown(id = 'end year', value = 2020, persistence_type='session', persistence=True),
            html.H6(" "),
            html.H6("Graph type:"),
            dcc.Dropdown(id = 'plot', value = 'stacked bar', options = ['Stacked Bar','Scatter Line'], persistence_type='session', persistence=True),
        ], className="sidebar"
            )
    ]
)

sidebar_map = html.Div(
    [
        dbc.Row(
            [
                html.H4('Options', className="sidebar"),
            ],
            style={"height": "5vh"}
            ),
        dbc.Row(
            [
                html.H6(" "),
                html.H6("Dataset:"),
                dcc.Dropdown(id = 'dataset', value = 'csa', persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Species:"),
                dcc.Dropdown(id = 'species-map', value = 'cattle', multi=False,persistence_type='session', persistence=True),
                html.H6(" "),
                html.H6("Year:"),
                dcc.Dropdown(id = 'year-map', value = 2020, persistence_type='session', persistence=True),
                ], className="sidebar"
            )
    ]
)

###-------------Components------------------------------------


title = html.Div([
                    html.Img(src=GBADSLOGOB, className="header-logo"),
                    html.H2('Ethiopia Livestock Population')
                ]
                )

tabs = html.Div([
    
    html.H1(" "),
    html.H2(" "),
        dbc.Tabs(
            [
                dbc.Tab(label="Graph", active_label_style=ACTIVE_TAB_STYLE),
                dbc.Tab(label="Map",active_label_style=ACTIVE_TAB_STYLE),
                dbc.Tab(label='Download Data', active_label_style=ACTIVE_TAB_STYLE),
                dbc.Tab(label='Metadata', active_label_style=ACTIVE_TAB_STYLE)
            ],
        id='tabs')
]
)

###--------------Build the layout------------------------------------

app_layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(title, width=6),
                dbc.Col(tabs, width='auto')
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(id='tabs-content'))
            ]
            ),
    ],
    fluid=True
    )
