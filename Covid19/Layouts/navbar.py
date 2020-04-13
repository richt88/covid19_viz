# Python Imports

# Dash Imports
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Import Dashboard Elements
from Covid19.server import app
from Covid19.data.ecdc_data import update_ecdc_data
from Covid19.data.uk_data import update_UK_counties_data
from Covid19.Layouts.create_animation import make_animation_file

# NavBar
PLOTLY_LOGO = r"https://cdn.pixabay.com/photo/2020/03/14/10/58/virus-4930250_960_720.jpg"


nav_buttons =  dbc.Row(
                        [ 
                          dbc.Col([dbc.Button('Data Sources',
                                              id='sources-button',
                                              color="secondary",
                                              className="ml-2")],
                                              width="auto"),
                          dbc.Col([dbc.Button('UK Gov Advice',
                                              id='gov-advice-button',
                                              href= "https://www.gov.uk/coronavirus",
                                              color="secondary",
                                              className="ml-2")],
                                              width="auto"),
                         dbc.Col([dbc.Button('Update Data',
                                              id='update-button',
                                              color="primary",
                                              className="ml-2")],
                                              width="auto"),
                        ],
                        no_gutters=True,
                        className="ml-auto flex-nowrap mt-3 mt-md-0",
                        align="center",
                    )

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    #dbc.Col(html.Img(src=PLOTLY_LOGO, height="50px")),
                    dbc.Col(dbc.NavbarBrand("Covid-19 Data Visualisation",
                                            className="ml-2",
                                            #style = {'font-family':'monospace',},
                                            )),
                ],
                align="center",
                no_gutters=True,
            ),
            href="",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(nav_buttons, id="navbar-collapse", navbar=True),
                
    ],
    color="dark",
    dark=True,
    )
            


sources = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Data Sources"),
                dbc.ModalBody(dcc.Markdown("""
                    ### Global Data
                    * Gobal deaths data from [ECDC](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide)
                    
                    ### UK Data
                    * UK cases and deaths taken from [Public Health England](https://www.gov.uk/government/publications/covid-19-track-coronavirus-cases)
                    * County boundaries from [ONS](https://data.gov.uk/dataset/cd97a8df-e2fe-4f3d-a60f-1f871a317d31/counties-and-unitary-authorities-december-2016-full-extent-boundaries-in-england-and-wales)
                    \(simplified using [mapshaper](https://mapshaper.org/) \)
                    * Population data from [ONS](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland)
                    
                    ### Economic Data
                    * Historic FTSE 100 data from [LSE](https://www.londonstockexchange.com/statistics/ftse/ftse.htm)
                    * Current FTSE 100 value from [Yahoo finance](https://finance.yahoo.com/quote/%5EFTSE%3FP%3DFTSE)
                """
                )),
                dbc.ModalFooter(
                    dbc.Button("Close",
                               id="sources-close",
                               className="ml-auto")
                ),
            ],
            id="sources",
        ),
    ]
)

# Callbacks
# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# open Data Sources
@app.callback(
    Output("sources", "is_open"),
    [Input("sources-button", "n_clicks"),
     Input("sources-close", "n_clicks")],
    [State("sources", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Callback to update data files and all plots
@app.callback(Output('data_div_ecdc','children'),
              [Input('update-button', 'n_clicks')])
def update_ecdc_data_call(n_clicks):

    # Update data
    update_ecdc_data()
    update_UK_counties_data()
    
    # Update anmiation file
    make_animation_file()

    return ''
