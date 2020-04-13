# Python Imports


# Dash Imports
import dash_core_components as dcc
import dash_html_components as html
import plotly.io as pio
pio.templates.default = "plotly_dark"


# Imports Dashboard Elements
from ..data.ecdc_data import get_ecdc_data


# Get data
df = get_ecdc_data()

country_list = []
for c in df['countriesAndTerritories'].unique():
    country_list.append({'label':'{}'.format(c.replace('_', ' ')), 'value':c})
    

dropdown_w = html.Div([
                    html.H4('Select countries:', 
                            #style={'paddingRight':'30px'}
                            ),
                    dcc.Dropdown(
                        id='dropdown',
                        options=country_list,
                        value=['United_Kingdom'],
                        multi=True,
                        style={
                               #'background-color':'black',
                               'color':'black'})],)