# Python Imports
from urllib.request import urlopen
import json
import pandas as pd
import os

# Dash Imports
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly.io as pio
pio.templates.default = "plotly_dark"

# Import Dashboard Components
from ..data.uk_data import get_UK_counties_data    

# Get current location
dir_path = os.path.dirname(os.path.realpath(__file__))


def get_uk_map():
    # Get GeoJSON data
    
    #   English Counties
    counties_json = r'Simplified_Counties_and_Unitary_Authorities_December_2016_Full_Extent_Boundaries_in_England_and_Wales.geojson'
    with open(os.path.join(dir_path, r'..\data\GeoJSON', counties_json), "r") as read_file:
        data_counties = json.load(read_file)
    
    for f in data_counties['features']: # Correct to plotly expected format
        f['id'] = f['properties']['ctyua16cd']
        
    #    Correct the area code for Dorset & Bournmouth
    for f in data_counties['features']:
        if 'Dorset' in f['properties']['ctyua16nm']:
            f['id'] = 'E06000059'
        elif 'Bournemouth' in f['properties']['ctyua16nm']:
            f['id'] = 'E06000058'
    
    #   UK countries
    countries_json = r'Simplified_Countries_December_2019_Boundaries_UK_BFC.geojson'
    with open(os.path.join(dir_path, r'..\data\GeoJSON', countries_json), "r") as read_file:
        data_countries = json.load(read_file)
    
    for f in data_countries['features']: 
        f['id'] = f['properties']['ctry19cd']
        

    
    
    # Get Coronavirus data
    df = get_UK_counties_data()
    df = df[df['Date']==df['Date'].max()] # Latest Data only
    df = df[df['Area Name']!='England']
    
    # Get cases as a ratio of population
    df['cases_per_10k'] = (df['Reported Cases'] / df['Population']) * 10000
    

    
    # Create plot
    fig = go.Figure(data = [go.Choroplethmapbox(geojson=d,
                                        locations=df['Area Code'],
                                        z=df['cases_per_10k'],
                                        colorscale="Jet",
                                        text = df['Area Name'],
                                        customdata = df['Reported Cases'],
                                        name = '',
                                        hovertemplate = ('<b>%{text}</b><br>' +
                                                         '<b>%{z:.1f}</b> Cases per 10k<br>' +
                                                         '<b>%{customdata:.,}</b> Cases reported'),
                                        # zmin=0, zmax=12,
                                        marker_opacity=0.8,
                                        marker_line_width=1) for d in [data_counties, data_countries]])
    fig.update_layout(mapbox_style="carto-darkmatter",
                      mapbox_zoom=4.3,
                      mapbox_center = {"lat": 54.8, "lon": -4},
                      geo=dict(
                                showframe=False,
                                showcoastlines=False,
                                projection_type='equirectangular',
                                #'orthographic',
                                showocean=True,
                                oceancolor='rgba(50, 50, 50, 0.5)'))
    fig.update_layout(margin={"r":10,"t":10,"l":10,"b":10},
                      #height=600,
                      
                      )
    #pyo.plot(fig, 'test.html' )
    return fig

