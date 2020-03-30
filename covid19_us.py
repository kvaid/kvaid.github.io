from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
import plotly.express as px
import datetime as dt

# https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv
input_url_base = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"

# current_date = dt.datetime.today().strftime ('%m-%d-%Y')
# process_date = current_date
# input_url = input_url_base + process_date + ".csv"

# ***************************************************************************************

def read_datafile(in_date):
    in_date = in_date.strftime('%m-%d-%Y') # convert from datetime format to string MM-DD-YYYY
    input_url = input_url_base + in_date + ".csv"
    in_df = pd.read_csv(input_url,dtype={"FIPS":str,'Confirmed':int})
    in_df.rename(columns = {"Admin2":"County","Country_Region":"Country","Province_State":"State","Last_Update":"Date","Long_":"Long","Combined_Key":"Location"}, inplace = True)  # rename the columns
    # process the 'Date' column to remove the H:M:S timestamp and just represent as "YYYY-MM-DD"
    #print(in_df['Date'])
    if (in_date == "03-22-2020"):
        in_df['Date'] = in_df['Date'].map(lambda x: dt.datetime.strptime(x, "%m/%d/%y %H:%M")) # convert to datetime format
    else:
        in_df['Date'] = in_df['Date'].map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")) # convert to datetime format

    in_df['Date'] = in_df['Date'].map(lambda x: x.strftime("%d-%m-%Y")) # convert to string format
    #in_df['Date'] = pd.to_datetime(in_df['Date'])   # after this, the 'Date' column is of type <pandas._libs.tslibs.timestamps.Timestamp>
    #in_df['Date'] = in_df['Date'].map(lambda ts: ts.strftime("%d-%m-%Y")) # after this, the 'Date' column is of type <Str>
    #in_df['Date'] = pd.to_datetime(in_df['Date'])   # after this, the 'Date' column is of type <pandas._libs.tslibs.timestamps.Timestamp>

    in_df = in_df.loc[in_df['Country']=='US'] # retain only US states, drop other countries
    
    in_df['FIPS'] = in_df['FIPS'].fillna("0").map(lambda x: str(x).zfill(5)) # if no FIPS code then use "0" and then format FIPS string to 5 digits
    in_df['Confirmed'] = in_df['Confirmed'].fillna(0.0) # fill null values with 0
    in_df['County'] = in_df['County'].fillna("None") # fill county column null values with "None"

    #in_df_us = in_df[['Date','FIPS','State','County','Location','Confirmed','Deaths','Recovered']].copy()
    in_df_us = in_df.drop(columns=['Country','Lat','Long','Active']).copy()
    #print(in_date,"\n",in_df_us.tail())
    return in_df_us

# ***************************************************************************************

start_date = dt.datetime(2020, 3, 22) # start with March 22, 2020 
current_date = dt.datetime.today() - dt.timedelta(days=1)
df_us = read_datafile(current_date)

prev_date = (dt.datetime.today() - dt.timedelta(days=1))

while (prev_date >= start_date):
    df_prev = read_datafile(prev_date)
    df_us = pd.concat([df_us, df_prev]) #concatenate dataframes
    df_us.reset_index(drop=True, inplace=True) # reset index
    prev_date = prev_date - dt.timedelta(days=1)

df_us = df_us.sort_values(['FIPS','Date'], ascending=[True,True])

df_us = df_us.loc[df_us['State'].isin(['Washington','New York','California','Florida','Louisiana','Michigan','Massachussets','Illinois'])] # retain only specific US states, drop other countries

df_us.to_csv("covid_fips.csv")

fig = px.choropleth_mapbox(df_us, 
                title="Progression on COVID-19 cases across US counties",
                geojson=counties, 
                locations='FIPS', 
                color='Confirmed',
                color_continuous_scale="Reds",
                range_color=(0,1000),
                mapbox_style="carto-positron", # stamen-watercolor,stamen-terrain,carto-positron
                zoom=4, center = {"lat": 37.0902, "lon": -95.7129}, # for continental US
                #zoom=7,center = {"lat": 47.75, "lon": -120.75}, # for Washington state
                opacity=0.5,
                hover_name=df_us['Location'],
                hover_data=["Confirmed"],
                labels={'Confirmed':'Confirmed cases'},
                animation_frame='Date', # column name to show range of animation frame
                animation_group='FIPS' # column name that is constant across animation_frame data
                )
                
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
