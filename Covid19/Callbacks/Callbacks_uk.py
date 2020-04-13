# Python Imports
import os
import matplotlib
import numpy as np

# Dash Imports
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.offline as pyo

# Import Dashboard Elements
from ..server import app
from ..data.uk_data import get_UK_counties_data  
from ..data.ftse_data import get_ftse_data
from ..Layouts.UK_map import get_uk_map 


dir_path = os.path.dirname(os.path.realpath(__file__))

# Mini-function to convert colour format
def rgb_to_255(rgb):
    return (int(rgb[0]*255), 
            int(rgb[1]*255),
            int(rgb[2]*255))


# Plot of global UK map
@app.callback(Output('uk-map','figure'),
              [Input('data_div_ecdc', 'children')])
def update_uk_map(data_div):
    
    fig = get_uk_map()
    
    return fig

# Unconfirmed Cases Location
@app.callback(Output('unconfirmed-cases','children'),
              [Input('data_div_ecdc', 'children')])
def update_unconfirmed(data_div):
    
    df = get_UK_counties_data()
    
    # Get Coronavirus data
    df = get_UK_counties_data()
    df = df[df['Date']==df['Date'].max()] # Latest Data only
    
    # Unconfirmed data
    unconfirmed_row = df[df['Area Name']=='Unconfirmed']
    unconfirmed = int(unconfirmed_row['Reported Cases'].values[0])

    # Date
    update_date = df['Date'].max().strftime("%d %B %Y")
    
    return (f'Location unconfirmed for {unconfirmed:,} deaths.' +
            '    Updated: ' + update_date)


# Cases plot for hover county
@app.callback(Output('county-graph','figure'),
              [Input('data_div_ecdc', 'children'),
               Input('uk-map', 'hoverData' )])
def update_county(data_div, hoverData):
    
    # Hover Data
    if hoverData is None:
        code = 'E92000001'
        county_name = 'England (Hover over counties for data)'
    else:
        code = hoverData['points'][0]['location']
        county_name = hoverData['points'][0]['text']
    
    
    # Make plot colour
    cmap = matplotlib.cm.get_cmap('tab20')
    indx = np.random.choice(range(20))
    color ='rgb' + str(rgb_to_255(cmap(indx)[:3]))
    
    # get Data
    df = get_UK_counties_data()
    df_county = df[df['Area Code']==code].sort_values('Date')
    

    # Create Data traces
    data =  go.Scatter(
                x=df_county['Date'],
                y=df_county['Reported Cases'],
                #text = df_country.index.strftime("%d %B %Y"),
                name=df_county['Area Name'].iloc[0],
                mode='lines',
                line={'color':color,
                      'width':4},
                opacity=1,
                #hovertemplate = '<br><b>%{text}</b><br>' + '<b>Total Deaths</b>: %{y}'
            )
    fig = go.Figure(data = data,
                    layout = go.Layout(
                                title=f'Reported Cases in {county_name}',
                                hovermode= 'closest',
                                template= 'plotly_dark',
                                xaxis= {'title':'Date',
                                        'range' : [df['Date'].min(),
                                                   df['Date'].max()]
                                        },
                                legend_orientation="h",
                                legend=dict(x=-.1, y=-0.4)))    

    return fig

# FTSE 100 Plot
@app.callback(Output('ftse-plot','figure'),
              [Input('data_div_ecdc', 'children'),
               Input('ftse_smooth_toggle', 'value')])
def update_ftse(data_div, smooth_bool):
    
    # FTSE 100 Data
    df = get_ftse_data()
    
    # Smooth data
    if smooth_bool:
        df['Covid Normalised'] = df['Covid Normalised'].rolling(5, center=True).mean()
        df['Housing Normalised'] = df['Housing Normalised'].rolling(5, center=True).mean()

    # Create Data traces
    traces = []
    names = ['Crash caused by Covid-19', '2008 Crash', 'Brexit Vote']
    alphas = [1, 0.8, 0.8]
    dashs = ['solid', 'dash', 'dash']
    widths = [3, 1, 1]
    texts = [df['Covid Actual Date'], df['2008 Actual Date'], df['Brexit Actual Date']]
    
    for i, col in enumerate(['Covid Normalised',
                             'Housing Normalised',
                             'Brexit Normalised']):
    
        traces.append(go.Scatter(
                    x=df.index.days,
                    y=df[col],
                    text = texts[i].dt.strftime("%d %B %Y"),
                    name=names[i],
                    mode='lines',
                    line={'width':widths[i],
                          'dash':dashs[i]},
                    opacity=alphas[i],
                    hovertemplate = '<br><b>%{text}</b><br>' + '%{y:.2f}%'
                ))
    fig = go.Figure(data = traces,
                    layout = go.Layout(
                                title=f'FTSE 100 Index',
                                hovermode= 'closest',
                                template= 'plotly_dark',
                                xaxis= {'title':'Days After Start of Crash',
                                        },
                                yaxis= {'title':'% Change in FTSE 100',
                                        },        
                                ))    

    return fig
