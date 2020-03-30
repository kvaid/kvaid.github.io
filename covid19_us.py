from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
import plotly.express as px
import datetime as dt

input_url_base = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"

current_date = dt.datetime.today().strftime ('%m-%d-%Y')
input_url = input_url_base + current_date + ".csv"

df = pd.read_csv(input_url,dtype={"FIPS":str,'Confirmed':int})

df.rename(columns = {"Admin2":"County","Country_Region":"Country","Province_State":"State","Last_Update":"Date","Long_":"Long","Combined_Key":"Location"}, inplace = True)  # rename the columns
# process the 'Date' column to remove the H:M:S timestamp and just represent as "YYYY-MM-DD"
df['Date'] = pd.to_datetime(df['Date'])   # after this, the 'Date' column is of type <pandas._libs.tslibs.timestamps.Timestamp>
df['Date'] = df['Date'].map(lambda ts: ts.strftime("%d-%m-%Y")) # after this, the 'Date' column is of type <Str>
df['Date'] = pd.to_datetime(df['Date'])   # after this, the 'Date' column is of type <pandas._libs.tslibs.timestamps.Timestamp>

# # retain only US states, drop other countries
df = df.loc[df['Country']=='US']
#df['FIPS'] = df['FIPS'].fillna(0.0).astype(str)
df['FIPS'] = df['FIPS'].map(lambda x: str(x).zfill(5)) 
df['Confirmed'] = df['Confirmed'].fillna(0.0)

#df_us = df[['Date','FIPS','State','County','Location','Confirmed','Deaths','Recovered']].copy()
df_us = df.drop(columns=['Country','Lat','Long','Active']).copy()
df_us.to_csv("covid_fips.csv")
print(df_us.head())

fig = px.choropleth_mapbox(df_us, 
                geojson=counties, 
                locations='FIPS', 
                color='Confirmed',
                color_continuous_scale="Bluered",
                range_color=(0,100),
                mapbox_style="carto-positron", # stamen-watercolor,stamen-terrain,carto-positron
                zoom=3.75, center = {"lat": 37.0902, "lon": -95.7129}, # for continental US
                #zoom=6,center = {"lat": 47.75, "lon": -120.75}, # for Washington state
                opacity=0.5,
                hover_name=df_us['Location'],
                hover_data=["Confirmed"],
                labels={'Confirmed':'Confirmed cases'}
                )
                
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()
