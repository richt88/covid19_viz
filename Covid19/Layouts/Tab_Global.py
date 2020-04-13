# Python Imports
import os

# Dash Imports
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html



dir_path = os.path.dirname(os.path.realpath(__file__))
animation_file = os.path.join(dir_path, 'pandemic_animation.html')
animation_html = html.Iframe(srcDoc = open(animation_file, 'r').read(),
                             style = {'height': 500,
                                      'width':'100%',
                                      'border-style':'none',
                                      'padding-bottom': 0})

##Tab 1 - Global Data Tab

tab_content = [ dbc.Row([
                          html.H4('Current Pandemic Situation',
                                     style={'padding-left': 30,
                                            'padding-top': 15,}),  
                        ]),  
                dbc.Row([
                        dbc.Col(html.Div([animation_html],
                                     style = {'height':'100%'}),
                                width=12,
                                lg=12,
                                xs=12)
                        ]),
                dbc.Row(dbc.Col(html.Div('', style={'height':10}), width=12)),
                dbc.Row([
                    dbc.Col(html.Div([dcc.Graph(id='global_deaths',
                                                figure = {},
                                                )], style={'height':'100%'}),
                             width=12,
                             lg=6,
                             xs=12),
    
                    dbc.Col(html.Div([dcc.Graph(id='global_mortality',
                                                figure = {},
                                            )], style={'height':'100%'}),
                             width=12,
                             lg=6,
                             xs=12),
                    ])
                
            ]
            #style={'height':'100%'})
                

# Put content into column
tab_content =  dbc.Row(
                    dbc.Col(
                            tab_content,
                            width=12,
                            style = {'padding-left':30,
                                     'padding-right':30},
                            ),
                    justify="center")


