from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc

#server = Flask('covid19')
app = Dash(#server=server,
           external_stylesheets=[dbc.themes.DARKLY],
           suppress_callback_exceptions=True)
server = app.server
