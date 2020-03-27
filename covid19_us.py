from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
import plotly.express as px

input_file = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-26-2020.csv"

df = pd.read_csv(input_file)

# df.rename(columns = {"Admin2":"County","Country_Region":"Country","Province_State":"State","Last_Update":"Date","Long_":"Long","Combined_Key":"Location"}, inplace = True)  # rename the columns
# # process the 'Date' column to remove the H:M:S timestamp and just represent as "YYYY-MM-DD"
# df['Date'] = pd.to_datetime(df['Date'])   # after this, the 'Date' column is of type <pandas._libs.tslibs.timestamps.Timestamp>
# df['Date'] = df['Date'].map(lambda ts: ts.strftime("%d-%m-%Y")) # after this, the 'Date' column is of type <Str>
# df['Date'] = pd.to_datetime(df['Date'])   # after this, the 'Date' column is of type <pandas._libs.tslibs.timestamps.Timestamp>

# # format FIPS column as int
# df['FIPS'] = df['FIPS'].fillna(0.0).astype(int)


# # add sum for confirmed, recovered, deaths, active for every state
# list_columns = ['Confirmed','Recovered','Deaths','Active']
# datecol = df['Date']   # extract date column and save it for reinsertion later
# print(datecol)

# df_us = df.groupby('State')[list_columns].sum()
# df_us.insert(loc=0, column='Date', value=datecol) # insert 'Date' column at the beginning
# df_us.to_csv("covid_us_groupby.csv")
# print(df_us.head())

# # retain only US states, drop other countries
df = df.loc[df['Country_Region']=='US']
df['FIPS'] = df['FIPS'].fillna(0.0).astype(int)
df['FIPS'] = df['FIPS'].fillna(0.0).astype(str)
df['FIPS'] = df['FIPS'].map(lambda x: str(x).zfill(5)) 
df['Confirmed'] = df['Confirmed'].fillna(0.0).astype(int)

df_us = df[['FIPS','Confirmed','Combined_Key']].copy()
df_us.to_csv("covid_fips.csv")

fig = px.choropleth_mapbox(df_us, geojson=counties, locations='FIPS', color='Confirmed',
                           color_continuous_scale="Bluered",
                           range_color=(0,100),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           hover_name=df_us['Combined_Key'],
                           hover_data=["Confirmed"],
                           labels={'Confirmed':'Confirmed cases'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
