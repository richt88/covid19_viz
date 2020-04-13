# Python Imports
from datetime import datetime
import pandas as pd
import os


# Dash Imports
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.io as pio
pio.templates.default = "plotly_dark"

from ..data.ecdc_data import get_ecdc_data


def get_animation(df):
    date_range = pd.date_range(start = '15/02/2020', end=datetime.today(), freq='D')
    df_reindex = (df[['countriesAndTerritories', 'cum_deaths', 'plot_colours']]
                        .groupby('countriesAndTerritories')
                        .apply(lambda x: x.reindex(date_range, method='ffill')))
    df_reindex['date'] = df_reindex.index.get_level_values(1)
    
    
    
    # Create Frames
    
    frames = []
    for dt, df_date in df_reindex.groupby('date'):
        df_date = df_date.sort_values('cum_deaths', ascending=False)
        df_date = df_date.head(8)
        df_date = df_date.sort_values('cum_deaths', ascending=True)
        
        bar = go.Bar(y = df_date['countriesAndTerritories'],
                     x = df_date['cum_deaths'],
                     orientation='h',
                     marker_color=df_date['plot_colours'])
        layout = go.Layout(title = "Most Affected Countries",
                           margin=dict(l=200),
                           annotations=[
                                go.layout.Annotation(
                                    text= dt.strftime("%d %B %Y"),
                                    align='left',
                                    showarrow=False,
                                    xref='paper',
                                    yref='paper',
                                    x=0.8,
                                    y=1.1,
                                    #bordercolor='black',
                                    borderwidth=0,
                                    font=dict(size=20),
                                )
                            ])
        frames.append(go.Frame(data = bar,
                               layout = layout))
    
    
    # PLot
    
        
    updatemenus = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 300,
                                              "redraw": True},
                                    "fromcurrent": True,
                                    "transition": {"duration": 300,
                                                   "easing": "linear"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }]
    
    
    fig = go.Figure(
        data=frames[0].data,
        layout=go.Layout(
            title="Most Affected Countries - Click Play Below",
            margin=dict(l=200),
            xaxis=dict(
                       range=[0, df_reindex['cum_deaths'].max()], autorange=False,
                       title = 'Total number of Deaths',
                       #type = 'log'
                       ),
            #sliders = sliders,
            updatemenus=updatemenus,
    
        )               ,
        frames= frames
    )
    
    return fig
    

def make_animation_file():
    
    # Get Data    
    df = get_ecdc_data()
    
    # Set Output
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_out = os.path.join(dir_path, 'pandemic_animation.html')
    
    fig = get_animation(df)
    pyo.plot(fig,
             filename=file_out,
             auto_open=False,
             auto_play=False)    
    


    
