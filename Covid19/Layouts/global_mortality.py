# Python Imports
from datetime import datetime

# Dash Imports
import plotly.graph_objs as go



## Global Deaths Plot

def get_global_mortality(df):
    fig = go.Figure()
    
    
    # Calculate Mortality
    # Cut down to most recent (already sorted)
    df_current = df.groupby('countriesAndTerritories').tail(1)
    # Remove countries that have not been significantly affected
    df_current = df_current[df_current['cum_deaths']>=20]
    # Calculate mortality
    df_current['mortality'] = (df_current['cum_deaths'] / 
                               df_current['cum_cases']) *100
    plot_colours = {'Asia' : 'Red',
                    'Europe': 'RoyalBlue',
                    'Africa': 'ForestGreen',
                    'Oceania': 'DarkOrange',
                    'North America': 'Gold',
                    'South America': 'SkyBlue'}
    
    
    # Plot per continent
    for cont, df_cont in df_current.groupby('Continent_Name'):
        
        
        fig.add_trace(
            go.Scatter(
                x=df_cont['cum_cases'],
                y=df_cont['mortality'],
                text = df_cont['countriesAndTerritories'],
                name = cont,
                opacity=0.8,
                mode='markers',
                marker=dict(color=plot_colours[cont],
                            size = 16,
                            opacity=0.8,),
                hovertemplate = ('<br><b>%{text}</b></br>' +
                                 'Mortality: %{y:.2f}%<br></br>' + 
                                 'Cases: %{x:,}')
                                 
                        )
                    )
    
    fig.update_layout(title='Global Mortality Rates*',
                      hovermode= 'closest',
                      template= 'plotly_dark',
                      xaxis= {'title':'Reported Cases'},
                      yaxis = {'title': 'Reported Mortality Rate (%)'},
                      xaxis_type="log",
                      #margin = {'b': 20},
                      annotations=[
                                go.layout.Annotation(
                                    text=('*Data based on reported cases.<br>' +
                                         ' Note: There are large uncertainties in theses mortality rates' +
                                         ' due to incomplete and inconsistent testing between populations.'),
                                    align='left',
                                    showarrow=False,
                                    xref='paper',
                                    yref='paper',
                                    x=-0.05,
                                    y=-0.25,
                                    #bordercolor='black',
                                    borderwidth=0
                                )
                            ]
                      )
    return fig