import pandas as pd
import numpy as np
import os, re
from datetime import datetime, timedelta


dir_path = os.path.dirname(os.path.realpath(__file__))

# Remove old files
def purge(dir_path, pattern):
    for f in os.listdir(dir_path):
        if re.search(pattern, f):
            os.remove(os.path.join(dir_path, f))

# Functions to clean data after download
def counties_data_cleaning(df):
    
    # Move Area Code to Column
    df.reset_index(inplace = True)
    
    # Convert to tidy format
    df = pd.melt(df,
                 id_vars=['Area Name', 'Area Code'],
                 var_name='Date',
                 value_name='Reported Cases')
    
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



# Update Local Files
def update_UK_counties_data():
    url = (r"https://fingertips.phe.org.uk/documents/Historic%20COVID-19%20Dashboard%20Data.xlsx")
    
    # For last 10 days try to download new data or use local data
    for day_delta in range(0,10):
        # Set number of days to go back
        today = datetime.today() - timedelta(days=day_delta)
        try:
            # Get local version
            file = os.path.join(dir_path, 'UK_counties_' + today.strftime("%Y-%m-%d") + ".csv")
            df = pd.read_csv(file, index_col=0)
            return None
        
        except FileNotFoundError:
            try:
                # Try to download data
                #   Counties
                counties_head_row = (pd.read_excel(url,
                                                  sheet_name = 'UTLAs',
                                                  index_col = None,
                                                  header=None)\
                                                  .iloc[:,0] == 'Area Code')\
                                                  .idxmax()  
                                                  
                df_counties = pd.read_excel(url,
                                           sheet_name = 'UTLAs',
                                           header=counties_head_row,
                                           parse_dates=True,
                                           index_col=0)
                #    Countries
                countries_head_row = (pd.read_excel(url,
                                                  sheet_name = 'Countries',
                                                  index_col = None,
                                                  header=None)\
                                                  .iloc[:,0] == 'Area Code')\
                                                  .idxmax()  
                
                df_countries = pd.read_excel(url,
                                           sheet_name = 'Countries',
                                           header=countries_head_row,
                                           parse_dates=True,
                                           index_col=0)
                
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
                return None
            except:
                pass
                

# Read Local Files
def get_UK_counties_data():

    for day_delta in range(0,10):
        try:
            today = datetime.today() - timedelta(days=day_delta)
            file = os.path.join(dir_path, 'UK_counties_' + today.strftime("%Y-%m-%d") + ".csv")
            df = pd.read_csv(file,
                     index_col=None,
                     parse_dates=True,
                     )        
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except FileNotFoundError:
            pass
    


if __name__=='__main__':
    dir_path = r'C:\Users\Rich\Desktop\Covid19_Dashboard\Covid19\data'
    update_UK_counties_data()