# Python Imports
import os

# Dash Imports
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

dir_path = os.path.dirname(os.path.realpath(__file__))

 

#### UK Data

tab_content =  [
        dbc.Row(dbc.Col([
                        dbc.Row([
                             html.H4('UK Reported Cases',
                                     style={'padding-left': 15,
                                            'padding-top': 15,}),  
                                ])],
                       width=12, md=12, xs=12),),
        dbc.Row(
            [   
                dbc.Col([dcc.Graph(id='uk-map',figure = {}),
                         html.Div('', 
                                  id= 'unconfirmed-cases',
                                  style={'height':20})],
                         width=6, lg=6, xs=12),
                dbc.Col([dcc.Graph(id='county-graph',figure = {}),],
                         width=6, lg=6, xs=12)
                        
#                dcc.Interval(id='world_map_interval',
#                             interval=1000*60*60),
            ]
                ),
        dbc.Row(dbc.Col(html.Div('', style={'height':30}), width=12)),
        dbc.Row(
            [   dbc.Col([
                        dbc.Row([
                             html.H4('Economic Impact',style={'padding-left': 15}),  
                                ])],
                       width=6, lg=6, xs=12),
                dbc.Col([
                        dbc.Row([
                             html.H5('Smoothing :',style={'padding-left': 15}),
                             html.H5('Raw ', style={'padding-left': 20}),
                             daq.ToggleSwitch(id = 'ftse_smooth_toggle'),
                             html.H5('Averaged (5 Day)')]),
                        ],
                     width=6, lg=6, xs=12),
                dbc.Col([
                        dcc.Graph(id='ftse-plot',figure = {}),
                         ],
                         width=12, md=12, xs=12),
                
            ]
                ),
        
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


