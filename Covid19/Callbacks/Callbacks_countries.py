# Python Imports


# Dash Imports
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go



# Import DSashboard Elements
from Covid19.server import app
from Covid19.data.ecdc_data import get_ecdc_data



# Define Callbacks

@app.callback(Output('worldmap-deaths', 'figure'),
              [Input('data_div_ecdc', 'children')])
def update_world_map(data_div):
    
    # # Get data
    df = get_ecdc_data()
    
    # df maps
    df_maps = df[df.index == df.index.max()]
    
    
    
    # world Map
    fig = go.Figure(data=go.Choropleth(
        locations = df_maps['countryterritoryCode'],
        z = df_maps['cum_deaths'],
        text = df_maps['countriesAndTerritories'],
        colorscale = 'Jet',
        autocolorscale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '',
        colorbar_title = 'Total Deaths',
        
    ))
    
    fig.update_layout(
        #title_text='Global Deaths',
        #height = 600,
        #width = 800,

        geo=dict(
            center=dict(lon=0, lat=0),
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
            #'orthographic',
            showocean=True,
            oceancolor='rgba(100, 100, 100, 0.5)',
        ),
        margin={"r":0,"t":10,"l":10,"b":10},
        annotations = [dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='',
            showarrow = False
        )]
    )
    
    return fig   


@app.callback(Output('cum_death_plot','figure'),
              [Input('dropdown','value'),
               Input('data_div_ecdc', 'children'),
               Input('log_toggle', 'value'),
               Input('smooth_toggle', 'value')])
def update_cum_deaths(country_list, data_div, log_bool, smooth_bool):
    
    # # Get data
    df = get_ecdc_data()
    
    # Create Data traces
    traces = []
    for i, c in enumerate(country_list):
        
        df_country = df[df['countriesAndTerritories']==c]
        color = df_country['plot_colours'].iloc[0]
        traces.append(
            go.Scatter(
                x=df_country['days_since_20_deaths'],
                y=df_country['cum_deaths'],
                text = df_country.index.strftime("%d %B %Y"),
                name=c,
                mode='lines',
                opacity=0.9,
                line={'color':color,},
                hovertemplate = '<br><b>%{text}</b><br>' + '<b>Total Deaths</b>: %{y}'
            )
        )
    fig = go.Figure(data = traces,
                    layout = go.Layout(
                                title='Cumulative Deaths',
                                hovermode= 'closest',
                                template= 'plotly_dark',
                                xaxis= {'title':'Days since 20th death',
                                        },
                                legend_orientation="h",
                                legend=dict(x=-.1, y=-0.4)))    
    if log_bool:
        fig.layout.yaxis = {'type':'log'}
    return fig




@app.callback(Output('daily_deaths_plot','figure'),
              [Input('dropdown','value'),
               Input('data_div_ecdc', 'children'),
               Input('log_toggle', 'value'),
               Input('smooth_toggle', 'value')])
def update_daily_deaths(country_list, data_div, log_bool, smooth_bool):
    # Get data
    df = get_ecdc_data()
    
    # Create Data traces
    traces = []
    for i, c in enumerate(country_list):
        
        df_country = df[df['countriesAndTerritories']==c]
        color = df_country['plot_colours'].iloc[0]
        
        if not smooth_bool:
            # Raw data
            traces.append(
                go.Scatter(
                    x=df_country['days_since_20_deaths'],
                    y=df_country['deaths'],
                    text = df_country.index.strftime("%d %B %Y"),
                    name=c,
                    mode='lines',
                    opacity=0.9,
                    showlegend=True,
                    line = {#'dash' : 'dot',
                            'width': 2,
                            'color': color,},
                    hovertemplate = ('<br><b>%{text}</b><br>' +
                                     '<b>Deaths</b>: %{y:,}')
                ))
        else:
            # Smoothed data
            traces.append(
                go.Scatter(
                    x=df_country['days_since_20_deaths'],
                    y=df_country['daily_deaths_smoothed'],
                    text = df_country.index.strftime("%d %B %Y"),
                    name=c,
                    mode='lines',
                    opacity=0.9,
                    showlegend=False,
                    line = {'color': color,
                            #'dash':'dot',
                            },
                    hovertemplate = ('<br><b>%{text}</b><br>' +
                                    '<b>Average Daily Deaths</b>: %{y:,.0f}')
                ))
        
    fig = go.Figure(data = traces,
                    layout = go.Layout(
                                title='Daily Deaths',
                                hovermode= 'closest',
                                template= 'plotly_dark',
                                xaxis= {'title':'Days since 20th death',
                                        },
                                legend_orientation="h",
                                legend=dict(x=-.1, y=-0.4)))        
    if log_bool:
        fig.layout.yaxis = {'type':'log'}        
       
    return fig



@app.callback(Output( 'country_data' , 'children'),
              [Input('worldmap-deaths', 'hoverData' ),
               Input('data_div_ecdc', 'children')])
def callback_maphover( hoverData, data_div ):
    
    # Get data
    df = get_ecdc_data()
       
    # df maps
    df_maps = df[df.index == df.index.max()]

    
    try:
        country=hoverData['points'][0]['text']
        data = df_maps[df_maps['countriesAndTerritories']==country].iloc[0]
        
        name = country.replace("_", " ")
        cases = data['cum_cases']
        deaths = data['cum_deaths']
        avg_daily_7day = data['daily_deaths_smoothed']
        date = str(data['day']) + "-" + str(data['month']) + "-" + str(data['year'])
    
        
        return [dcc.Markdown(f"**{name}:**  "),
                dcc.Markdown(f"""Reported Cases:  {cases:,}  
                            Reported Deaths:  {deaths:,}  
                            Average daily deaths:  {avg_daily_7day:.0f}
                            """),
                dcc.Markdown(f"""*Average based on last 3 days.*   
                             *Data as of {date}*.
                            """),
                html.Div('Click country to add/remove from plots below.',
                        style = {'fontSize': 12})]
    except:
        return 'Hover over country for details.'


@app.callback(Output( 'dropdown' , 'value'),
              [Input('worldmap-deaths', 'clickData' )],
               [State('dropdown', 'value')])
def callback_mapclick( clickData, dropdown_values ):

    try:
        dropdown_set = set(dropdown_values)
        country = clickData['points'][0]['text']
        country_set = set([country])
        
        if country in dropdown_set:
            dropdown_set = dropdown_set - country_set
        else:
            dropdown_set = dropdown_set | country_set
            
        return list(dropdown_set)
    except:
        return dropdown_values
    
    