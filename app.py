import os
import dash 
import dash_bootstrap_components as dbc 

app = None
if 'DASH_BASE_URL' in os.environ:
    app = dash.Dash(
        __name__,
        title='GBADs Ethiopia Regions Population Dashboard V1',
        external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.themes.LUX],
        requests_pathname_prefix=os.environ['DASH_BASE_URL']+'/'
    )
else:
    app = dash.Dash(
        __name__,
        title='GBADs Ethiopia Regions Population Dashboard V1',
        external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.themes.LUX]
    )
