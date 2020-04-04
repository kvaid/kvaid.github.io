from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
import plotly.express as px
import plotly
import datetime as dt

# Github repo: https://github.com/nytimes/covid-19-data
# file format
# date,county,state,fips,cases,deaths
# 2020-01-21,Snohomish,Washington,53061,1,0
# 2020-01-22,Snohomish,Washington,53061,1,0
df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",dtype={"fips":str,"cases":int,"deaths":int})

df['date'] = df['date'].map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d")) # convert to datetime format
df['date'] = df['date'].map(lambda x: x.strftime("%m-%d-%Y")) # convert to string format

# the file has some exceptions that we need to handle before further processing
# NYC ... All cases for the five boroughs of New York City (New York, Kings, Queens, Bronx and Richmond counties) are assigned to a single area called New York City.
# Kansas City, Mo. .... Four counties (Cass, Clay, Jackson and Platte) overlap the municipality of Kansas City, Mo. The cases and deaths that we show for these four 
#                       counties are only for the portions exclusive of Kansas City. Cases and deaths for Kansas City are reported as their own line.
# 
# FIPS codes to be inserted in df
# NYC: 36061

df['fips'] = df['fips'].fillna("0").map(lambda x: str(x).zfill(5)) # if no FIPS code then use "0" and then format FIPS string to 5 digits
df.loc[df['county']=='New York City','fips'] = "36061" # select rows that match "New York City" for 'county' column, and replace all 'fips' column values with "36061"
df = df[df['cases'] > 40] # retain only rows with 'cases' greater than 10
#df = df.reset_index()

df.to_csv("output/covid19_us_counties_nytimes.csv")

#df = df.loc[df['state'].isin(['Washington','New York','California','Florida','Louisiana','Michigan','Massachussets','Illinois'])] # retain only specific US states, drop other countries
#df = df.loc[df['state'].isin(['Washington','California'])] # retain only specific US states, drop other countries

fig = px.choropleth_mapbox(df, 
                title="Progression of COVID-19 cases across US counties (>35 cases per county)",
                geojson=counties, 
                locations='fips', 
                color='cases',
                color_continuous_scale="Reds",
                range_color=(0,1000),
                mapbox_style="carto-positron", # stamen-watercolor,stamen-terrain,carto-positron
                zoom=4.5, center = {"lat": 37.0902, "lon": -95.7129}, # for continental US
                #zoom=7,center = {"lat": 47.75, "lon": -120.75}, # for Washington state
                opacity=0.5,
                hover_name=df['county'],
                #hover_data=['cases'],
                #labels={'cases':'Confirmed cases'},
                animation_frame='date', # column name to show range of animation frame
                animation_group='fips' # column name that is constant across animation_frame data
                )
                
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
fig.write_html('index.html', auto_open=True)

