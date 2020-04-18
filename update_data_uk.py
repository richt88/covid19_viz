import pandas as pd
import os, re
from datetime import datetime


dir_path = r'/home/richt88/covid19_viz/Covid19/data/'

# Remove old files
def purge(dir_path, pattern):
    for f in os.listdir(dir_path):
        if re.search(pattern, f):
            os.remove(os.path.join(dir_path, f))

# Functions to clean data after download
def counties_data_cleaning(df):

    # Move Area Code to Column
    #df.reset_index(inplace = True)

    # Convert to tidy format
    #df = pd.melt(df,
    #             id_vars=['Area Name', 'Area Code'],
    #             var_name='Date',
    #             value_name='Reported Cases')

    # Get population data
    df_pop = pd.read_csv(os.path.join(dir_path, 'UK_pop_2019.csv'))

    df_pop['All ages'] = df_pop['All ages'].str.replace(",","")
    df_pop = df_pop.astype({'All ages':'int32'})
    df = df.merge(df_pop[['Code', 'All ages']],
                 how='left',
                 left_on='Area Code',
                 right_on='Code',
                 )
    df.rename({'All ages':'Population'},
              axis=1,
              inplace=True)


    # Remove trailing spaces
    df['Area Name'] = df['Area Name'].str.strip()


    return df



# Site moved and no auto access possible
# url = (r"https://fingertips.phe.org.uk/documents/Historic%20COVID-19%20Dashboard%20Data.xlsx")

# Local copy taken
file_path = r'/home/richt88/covid19_viz/Covid19/data/coronavirus-cases.csv'

today = datetime.today()

# Import local data
df_all_cases = pd.read_csv(file_path,
                           index_col=None,
                           parse_dates=True
                            )

# Correct column names to match previous gov version the code expects
df_all_cases.rename(columns={'Cumulative lab-confirmed cases':'Reported Cases',
                              'Specimen date':'Date',
                              'Area code':'Area Code',
                              'Area name': 'Area Name'},
                              inplace = True)

#   Counties
df_counties = df_all_cases[df_all_cases['Area type']!='Country']

#    Countries
df_countries = df_all_cases[df_all_cases['Area type']=='Country']

# Apply transformations
df_counties = counties_data_cleaning(df_counties)
df_countries = counties_data_cleaning(df_countries)

#   Combine
df = df_countries.append(df_counties)

#   Remove UK
df = df[df['Area Name']!='UK']

#   Remove rows with reported data missing
df = df.dropna(subset=['Reported Cases'])


# Remove old files
pattern = r'^UK_counties_.*csv'
purge(dir_path, pattern)

# Save to File
file = os.path.join(dir_path, 'UK_counties_' + today.strftime("%Y-%m-%d") + ".csv")

df.to_csv(file,
        index=False)

