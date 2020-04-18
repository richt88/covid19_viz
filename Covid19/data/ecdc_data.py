import pandas as pd
import os, re
from datetime import datetime, timedelta
import numpy as np


import matplotlib


dir_path = '/home/richt88/covid19_viz/Covid19/data/'

# Remove old files
def purge(dir_path, pattern):
    for f in os.listdir(dir_path):
        if re.search(pattern, f):
            os.remove(os.path.join(dir_path, f))

def data_cleaning(df):

    #
    df['countriesAndTerritories'].replace(
                to_replace='Cases_on_an_international_conveyance_Japan',
                value= 'Diamond Princess cruise ship',
                inplace = True)
    # Sort Values
    df.sort_values(['countriesAndTerritories', 'year', 'month', 'day'],
                   inplace=True)

    # Cumulative Cases & Deaths
    df['cum_cases'] = df.groupby('countriesAndTerritories')['cases'].cumsum()
    df['cum_deaths'] = df.groupby('countriesAndTerritories')['deaths'].cumsum()

    # Shifted to time since 20th death
    df['over_20'] = df['cum_deaths'] >= 20
    df['days_since_20_deaths'] = df.groupby('countriesAndTerritories')['over_20'].cumsum()

    # Rate of Increase

    df['daily_deaths_smoothed'] = df['deaths'].rolling(3, center=False).mean()
    df['daily_cases_smoothed'] = df['cases'].rolling(3, center=False).mean()

    # Add Continents
    dir_path = os.path.dirname(os.path.realpath(__file__))

    df_continents = pd.read_csv(os.path.join(dir_path, 'Continent_country.csv'))
    df.reset_index(inplace=True)
    df = df.merge(df_continents,
                  how='left',
                  left_on='countryterritoryCode',
                  right_on='Three_Letter_Country_Code')
    df.set_index('dateRep')

    # Add plot colours
    def rgb_to_255(rgb):
        return (int(rgb[0]*255),
                int(rgb[1]*255),
                int(rgb[2]*255))

    np.random.seed(2)
    unique_countries = list(df.sort_values('cum_deaths', ascending=False)['countryterritoryCode'].unique())
    # Top 20 countries (make sure the colors are distinct)
    cmap = matplotlib.cm.get_cmap('tab20')
    indx = np.random.choice(range(20), replace=False, size=20)
    plot_colours = {c : 'rgb' + str(rgb_to_255(cmap(indx[i])[:3])) for i, c in enumerate(unique_countries[:20])}
    # Create the rest
    cmap = matplotlib.cm.get_cmap('gist_rainbow')
    plot_colours.update({c : 'rgb' + str(rgb_to_255(cmap(np.random.rand())[:3])) for c in unique_countries[20:]})


    df['plot_colours'] = [plot_colours[c] for c in df['countryterritoryCode']]


    return df



# Import world data
def update_ecdc_data():
    url = ("https://www.ecdc.europa.eu/sites/default/files/documents/" +
           "COVID-19-geographic-disbtribution-worldwide-")


    # For last 10 days try to download new data or use local data
    for day_delta in range(0,10):
        # Set number of days to go back
        today = datetime.today() - timedelta(days=day_delta)
        try:
            # Check if local file is there
            file = os.path.join(dir_path, 'COVID-19' + today.strftime("%Y-%m-%d") + ".csv")
            df = pd.read_csv(file, index_col=0)
            return None
        except :
            try:
                # Try to download todays data
                url_full = url + today.strftime("%Y-%m-%d") + ".xlsx"
                df = pd.read_excel(url_full,
                                   index_col=0)

                # Remove old files
                pattern = r'^COVID-19.*csv'
                purge(dir_path, pattern)

                # Save New file
                file = os.path.join(dir_path, 'COVID-19' + today.strftime("%Y-%m-%d") + ".csv")
                df = data_cleaning(df)
                df.to_csv(file,
                          index=False)
                return df


            except:
                pass




def get_ecdc_data():


    for day_delta in range(0,10):
        try:
            today = datetime.today() - timedelta(days=day_delta)
            file = os.path.join(dir_path, 'COVID-19' + today.strftime("%Y-%m-%d") + ".csv")
            df = pd.read_csv(file,
                     index_col=0,
                     parse_dates=True,
                     )
            return df
        except :
            pass


if __name__=='__main__':
    update_ecdc_data()

