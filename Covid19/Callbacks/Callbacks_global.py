# Python Imports
from datetime import datetime
import random
import numpy as np
import pandas as pd


# Dash Imports
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

# Import Dashboard Elements
from ..server import app
from ..data.ecdc_data import get_ecdc_data
from ..Layouts.global_deaths import get_global_deaths
from ..Layouts.global_mortality import get_global_mortality



# Plot of global deaths vs time
@app.callback(Output('global_deaths','figure'),
              [Input('data_div_ecdc', 'children')])
def update_global_deaths(data_div):
    
    # Get data
    df = get_ecdc_data()
    
    
    fig = get_global_deaths(df)
    
    return fig


# Plot of global mortality rates
@app.callback(Output('global_mortality','figure'),
              [Input('data_div_ecdc', 'children')])
def update_global_mortality(data_div):
    
    # Get data
    df = get_ecdc_data()
    
    
    fig = get_global_mortality(df)
    
    return fig



