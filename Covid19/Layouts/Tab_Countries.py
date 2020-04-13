# Python Imports


# Dash Imports
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

# Dashboard elements
from .dropdown_world import dropdown_w



 

#### Global Data

tab_content =  [
                 dbc.Row([
                          html.H4('Global Deaths',
                                     style={'padding-left': 30,
                                            'padding-top': 15,}),  
                        ]),
                dbc.Row([   
                         dbc.Col(dcc.Graph(id='worldmap-deaths',
                                              figure = {}), width=8, md=8, xs=12),
                         dcc.Interval(id='world_map_interval',
                                         interval=1000*60*60),
                         dbc.Col(html.Div('Hover over country for details.', 
                                             id='country_data'), 
                                    width=4, md=4, xs=12),
                        ]),
        dbc.Row(dbc.Col(html.Div('', style={'height':20}), width=12)),
        dbc.Row([dbc.Col([dropdown_w], width=8, md=8, xs=12)]),
        dbc.Row(dbc.Col(html.Div('', style={'height':15}), width=12)),
        dbc.Row(
                [dbc.Col([
                        dbc.Row([
                             html.H5('Scale :\t\t',style={'padding-left': 15}),
                             html.H5('Linear ', style={'padding-left': 20}),
                             daq.ToggleSwitch(id = 'log_toggle'),
                             html.H5(' Log')])
                        ,],
                     width=6, lg=6, xs=12),
                dbc.Col([
                        dbc.Row([
                             html.H5('Smoothing :',style={'padding-left': 15}),
                             html.H5('Raw ', style={'padding-left': 20}),
                             daq.ToggleSwitch(id = 'smooth_toggle'),
                             html.H5(' Averaged (last 3 days)')]),
                        ],
                     width=6, lg=6, xs=12)
                ]),
        dbc.Row(
            [dbc.Col(html.Div([dcc.Graph(id='cum_death_plot',
                                  figure = {})]), width=6, lg=6, xs=12),
                dbc.Col(html.Div([dcc.Graph(id='daily_deaths_plot',
                                  figure = {})]), width=6, lg=6, xs=12),
            ],
                justify="start"),
        ]
             

# Put content into column
tab_content =  dbc.Row(
                    dbc.Col(
                            tab_content,
                            width=12,
                            style = {'padding-left':30,
                                     'padding-right':30},
                            ),
                    justify="center")




