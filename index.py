import os
import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import json
from dash.exceptions import PreventUpdate

from app import app
from layouts import layout, data_tab, graph_tab, metadata_tab, map_tab

###--------------Read in data-----------------------------------

csa = pd.read_csv('data/csa.csv')
cattle = pd.read_csv('data/cattle.csv')
camels = pd.read_csv('data/camels.csv')
poultry = pd.read_csv('data/poultry.csv')

def get_df(choice): 

    if choice == 'csa': 
        return(csa)
    elif choice == 'cattle':
        return(cattle)
    elif choice == 'camels':
        return(camels)
    elif choice == 'poultry':
        return(poultry)

def prep_df(df, region, species, start, end): 

    # Determine types 
    if type(region) == str: 
        df = df[df['region'] == region]
    else: 
        df = df[df['region'].isin(region)]
    
    if type(species) == str: 
        df = df[df['species'] == species]
    else: 
        df = df[df['species'].isin(species)]

    df = df[df['year'].between(start,end)]

    return(df)
    
app.layout = layout.app_layout

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'active_tab')])
def render_content(tab):
    if tab == 'tab-0':
        return graph_tab.content
    elif tab == 'tab-1':
        return map_tab.content
    elif tab == 'tab-2':
       return data_tab.content
    elif tab == 'tab-3':
        return metadata_tab.metadata_content

# Organize options of selecting multiple
@app.callback(
    Output('region','multi'),
    Output('species','multi'),
    Input('tabs','active_tab'),
    Input('choice','value')
)
def update_multiples(at, choice):

    if choice == 'Species': 
        return(False, True)
    else: 
        return(True, False)
      
@app.callback(
    Output('region','options'),
    Output('species','options'),
    Output('start year','options'),
    Output('end year','options'),
    Input('dataset','value'),
)
def update_all_dd(data):
    df = get_df(data)
    region_options = df['region'].unique().tolist()
    species_options = df['species'].unique().tolist()
    df = df.sort_values(by=['year'])
    years = df['year'].unique()
    return(region_options, species_options, years, years)

# Initialize dataset dropdown
@app.callback(
    Output('dataset','options'),
    Input('tabs','active_tab'),
)
def dataset_drop(at):

    dataset_options = ['csa', 'cattle', 'camels', 'poultry']

    return(dataset_options)

# Display metadata 
@app.callback(
    Output('metadata-table','data'),
    Input('dataset','value'),
    Input('tabs','active_tab')
)
def get_metadata(data, at):
    
    df = metadata_tab.get_metadata_df(data)

    return df.to_dict('records')

# Display graph
# Update graph
@app.callback(
    Output('graph1','figure'),
    Input('region','value'),
    Input('species','value'),
    Input('start year', 'value'),
    Input('end year', 'value'),
    Input('dataset','value'),
    Input('plot','value'))
def update_graph(region, species, start, end, data, plot):

    if type(region) == list and type(species) == list:
        raise PreventUpdate

    df = get_df(data)
    df = prep_df(df, region, species, start, end)

    if plot == 'stacked bar':
        fig = graph_tab.create_bar_plot(df, region, species)
    elif plot == 'scatter line':
        fig = graph_tab.create_scatter_plot(df, region, species)

    return(fig)

# Update data table 
@app.callback(
    Output('datatable','data'),
    Output('datatable','columns'),
    Input('dataset','value'),
    Input('region','value'), 
    Input('species','value'),
    Input('start year', 'value'),
    Input('end year', 'value'),
    )
def update_table(data, region, species, start, end):

    df = get_df(data)
    df = prep_df(df, region, species, start, end)
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]

# Update map
# Update year option on map tab
@app.callback(
    Output('species-map','options'),
    Output('year-map','options'),
    Input('dataset','value'),
)
def update_species_map(data): 

    df = get_df(data)
    
    species = df['species'].unique()
    df = df.sort_values(by=['year'])
    year = df['year'].unique()

    return(species, year)

@app.callback(
    Output('map','figure'),
    Input('dataset','value'),
    Input('species-map','value'),
    Input('year-map', 'value'),
    )
def update_map(data, species, year):

    df = get_df(data)
    merged_df = df.loc[df['year'] == year]
    merged_df = merged_df.loc[merged_df['species'] == species]

    fig = map_tab.create_map(merged_df, data, species, year)

    return(fig)

if __name__ == '__main__':
    app.run_server(debug=False)
    app.config['suppress_callback_exceptions'] = True

# return the wsgi app
def returnApp():
    """
    This function is used to create the app and return it to waitress in the docker container
    """
    # If BASE_URL is set, use DispatcherMiddleware to serve the app from that path
    if 'BASE_URL' in os.environ:
        from flask import Flask
        from werkzeug.middleware.dispatcher import DispatcherMiddleware
        app.wsgi_app = DispatcherMiddleware(Flask('dummy_app'), {
            os.environ['BASE_URL']: app.server
        })
        # Added redirect to new path
        @app.wsgi_app.app.route('/')
        def redirect_to_dashboard():
            from flask import redirect
            return redirect(os.environ['BASE_URL'])
        return app.wsgi_app

    # If no BASE_URL is set, just return the app server
    return app.server
