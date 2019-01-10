import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import os


#Data
#Data for countries (simplified version)
df = pd.read_csv('./Data/WDI_csv/EN_EG_data.csv')
#Data for the complete version insert the WDI dataset of https://datacatalog.worldbank.org/dataset/world-development-indicators here
#df = pd. read_csv('./Data/WDI_csv/WDIData.csv')
countries = pd.read_csv('./Data/countries.csv')['ISO']

#Negative values are replaced by 'nan'
for col in list(df)[list(df).index('1960'):list(df).index('2017')+1]:
    df.loc[~(df[col] > 0), col] = np.nan

#Extract data of the 177 countries from above (I end up with 168 countries only...)
df = df[df['Country Code'].isin(countries)].copy()




app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')