import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
import numpy as np
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

def get_ftse_data():
     # Recent Data
    yahoo_url = (r'https://query1.finance.yahoo.com/v7/finance/download/%5EFTSE?P=FTSE?period1=1176249600&period2=' +
                 str(int(time.time())) + 
                 '&interval=1d&events=history')
    
    df_yahoo = pd.read_csv(yahoo_url,
                           index_col = 0,
                           parse_dates = True).sort_index()
    
    # Started 2020, 02, 27
    covid_crash_date = datetime(2020, 2, 21)
    df_crash_covid = df_yahoo[df_yahoo.index >= covid_crash_date]
    pre_crash_value = df_crash_covid.loc[covid_crash_date]['Open']
    df_crash_covid['Covid Normalised'] = 100 * (df_crash_covid['Open'] - pre_crash_value) / pre_crash_value
    df_crash_covid['Days since crash'] = df_crash_covid.index - covid_crash_date
    
    
    # Historic Data
    df_lse = pd.read_csv(os.path.join(dir_path, 'FTSE_historic.csv'),
                         index_col = 0,
                         parse_dates = True).sort_index()
    
    # 2008 Crash
    # Started 2007, 12, 22
    housing_crash_date = datetime(2007, 12, 26)
    df_crash = df_lse[df_lse.index >= housing_crash_date]
    pre_crash_value = df_crash.iloc[0]['FTSE 100']
    df_crash['Housing Normalised'] = 100 * (df_crash['FTSE 100'] - pre_crash_value) / pre_crash_value
    df_crash['Days since crash'] = df_crash.index - housing_crash_date

    # Brexit Vote
    # Started 2016, 6, 23
    brexit_crash_date = datetime(2016, 6, 23)
    df_brexit = df_lse[df_lse.index >= brexit_crash_date]
    pre_crash_value = df_brexit.iloc[0]['FTSE 100']
    df_brexit['Brexit Normalised'] = 100 * (df_brexit['FTSE 100'] - pre_crash_value) / pre_crash_value
    df_brexit['Days since crash'] = df_brexit.index - brexit_crash_date    
    
    # Combine Data
    days_since_covid_crash = df_crash_covid['Days since crash'].max()
    days_to_include = days_since_covid_crash + timedelta(days=28)

    df_crash = df_crash[df_crash['Days since crash']<days_to_include]
    df_brexit = df_brexit[df_brexit['Days since crash']<days_to_include]
    
    # Merge Historic
    df_FTSE = df_crash[['Days since crash', 'Housing Normalised']]
    df_FTSE = df_FTSE.merge(df_brexit[['Days since crash', 'Brexit Normalised']],
                            on='Days since crash',
                            how = 'outer')
    # Merge Recent
    df_FTSE = df_FTSE.merge(df_crash_covid,
                            on='Days since crash',
                            how = 'outer')\
                     .sort_values('Days since crash')\
                     .set_index('Days since crash')\
                     .fillna(method='ffill')
    df_FTSE.loc[df_FTSE.index > days_since_covid_crash, 'Covid Normalised'] = np.nan      
    
    df_FTSE['Covid Actual Date'] =  covid_crash_date + df_FTSE.index
    df_FTSE['2008 Actual Date'] =  housing_crash_date + df_FTSE.index
    df_FTSE['Brexit Actual Date'] =  brexit_crash_date + df_FTSE.index
    
    return df_FTSE