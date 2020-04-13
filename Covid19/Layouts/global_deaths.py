# Python Imports
from datetime import datetime

# Dash Imports
import plotly.graph_objs as go


plot_colours = {'Asia' : 'Red',
                'Europe': 'RoyalBlue',
                'Africa': 'ForestGreen',
                'Oceania': 'DarkOrange',
                'North America': 'Gold',
                'South America': 'SkyBlue'}
## Global Deaths Plot

def get_global_deaths(df):
    fig = go.Figure()
    
    
    
    
    for cont, df_cont in df.groupby('Continent_Name'):
        df_cont_time = df_cont.groupby('dateRep').sum()
    
        fig.add_trace(
            go.Scatter(
                x=df_cont_time.index,
                y=df_cont_time['cum_deaths'],
                text = [cont]*len(df_cont_time),
                name= cont,
                mode='lines',
                line = dict(color=plot_colours[cont]),
                stackgroup='one',
                hovertemplate = '<b>%{text} Deaths</b>: %{y:,}'
                        )
                    )
    
    fig.update_layout(title='Global Deaths',
                      hovermode= 'closest',
                      template= 'plotly_dark',
                      xaxis= {'title':'Date'},
                      #legend_orientation="h",
    #                      legend=dict(x=-.1, y=-0.4),
                      xaxis_range=[datetime(2020, 3, 8),
                                   df_cont_time.index.max()],
                     legend={'traceorder':'normal'} # match order in mortality plot
                      )
    return fig