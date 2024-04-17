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
from layouts import layout, comments_section

def create_bar_plot(df, region, species):

    if type(region) == str:
        color_by = 'species'
        title = 'Population of Livestock in %s' % region
    else: 
        color_by = 'region'
        title = 'Population of %s' % species

    fig = px.bar(df, x='year', y='population', color=color_by,
                 color_discrete_sequence=px.colors.qualitative.Plotly, title = title)

    fig.update_xaxes(
        
        ticklabelmode="period",
        dtick = 1)

    return(fig)

def create_scatter_plot(df, region, species): 

    if type(region) == str:
        color_by = 'species'
        title = 'Population of Livestock in %s' % region
    else: 
        color_by = 'region'
        title = 'Population of %s' % species

    fig = px.line(df, x='year', y='population', color=color_by,
                 color_discrete_sequence=px.colors.qualitative.Plotly, markers=True, title = title)

    fig.update_xaxes(
        
        ticklabelmode="period",
        dtick = 1)
    
    return(fig)

graph = dcc.Graph(id = 'graph1', config = layout.plot_config)

content = dbc.Row(
    [
        dbc.Col(layout.sidebar, 
                xs=dict(order=1, size=12),
                sm=dict(order=1, size=3)
                ),
        dbc.Col(
            [graph, comments_section.comment_area],
                xs=dict(order=2, size=12),
                sm=dict(order=2, size='auto'))
    ], className='root-container'
)

