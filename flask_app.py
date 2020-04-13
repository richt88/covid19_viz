# Update Data Files
from Covid19.data.ecdc_data import update_ecdc_data
from Covid19.data.uk_data import update_UK_counties_data
# Get latest data
update_ecdc_data()
update_UK_counties_data()

# Create animation file
from Covid19.Layouts.create_animation import make_animation_file
make_animation_file()

# Python Imports


# Dash Imports
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output



# Import App
from Covid19.server import app
server = app.server


# Import Layout
from Covid19.Layouts.navbar import navbar, sources
from Covid19.Layouts.Tab_Countries import tab_content as tab_countries
from Covid19.Layouts.Tab_Global import tab_content as tab_global
from Covid19.Layouts.Tab_UK import tab_content as tab_uk




# Import Callbacks
from Covid19.Callbacks.Callbacks_countries import *
from Covid19.Callbacks.Callbacks_global import *
from Covid19.Callbacks.Callbacks_uk import *


## Define Layout

tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Global Data", tab_id="tab-1"),
                dbc.Tab(label="Countries", tab_id="tab-2"),
                dbc.Tab(label="UK Data", tab_id="tab-3"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)




app.layout = dbc.Container(
                        [html.Div(id='data_div_ecdc', style={'display': 'none'}),
                         navbar,
                         sources,
                         # Sub-title
                         dbc.Row(
                                    [
                                        dbc.Col(html.Div("Stay Home."), width=4),
                                        dbc.Col(html.Div("Protect the NHS."), width=4),
                                        dbc.Col(html.Div("Save Lives."), width=4),
                                    ],
                                    justify="center",
                                    style = {'padding-bottom': 10,
                                             'padding-top': 20,
                                             'color':'rgb(200,200,200)',
                                             'font-size': 20,
                                             'font-weight': 'bold',
                                             'text-align': 'center'}

                                ),
                         # Import Tabs
                         tabs
                         ],
                         fluid=True,
                    )



# Callbacks
@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab_global
    elif at == "tab-2":
        return tab_countries
    elif at == "tab-3":
        return tab_uk
    return html.P("This shouldn't ever be displayed...")
