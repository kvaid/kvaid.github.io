# https://plotly.com/python/mapbox-county-choropleth/

import plotly
import plotly.express as px

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})
print(df.head())

# all parameters at https://plotly.github.io/plotly.py-docs/generated/plotly.express.choropleth_mapbox.html
fig = px.choropleth_mapbox(df, 
                geojson=counties, # list of US county locations
                locations='fips', # column name with location info
                color='unemp', # column name to display
                color_continuous_scale="Viridis", # from https://plotly.com/python/builtin-colorscales/
                range_color=(0, 12), # range of color scale
                mapbox_style="carto-positron", # stamen-watercolor,stamen-terrain,carto-positron
                #zoom=3.75, center = {"lat": 37.0902, "lon": -95.7129}, # for continental US
                zoom=6,center = {"lat": 47.75, "lon": -120.75}, # for Washington state
                opacity=0.5,
                labels={'unemp':'unemployment rate'}
                )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()