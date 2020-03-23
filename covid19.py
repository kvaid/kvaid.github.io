import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
#import plotly.express as px
import plotly.graph_objs as go

#df = pd.read_csv("covid19.csv")
df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
df.rename(columns = {"Country/Region":"country","Province/State":"state"}, inplace = True)  # rename the columns
# bool_usa = (df.country == 'US')               # create boolean array for rows listed with country==US
# df_usa = df[bool_usa].reset_index(drop=True)   # create new dataframe for US items and reset index to start at 0
# bool_state = df_usa.state.isin(['Washington','California','New York'])
# df_state = df_usa[bool_state].reset_index(drop=True)

df.loc[df['state'].notnull(),'country'] = df['country'] + ' ' + df['state']
df = df.drop(['state','Lat','Long'], axis=1)
df = df.set_index('country')
# print(df.iloc[0:10,0:5])

dft = df.T                                          # Transpose
dft = dft.reset_index()                             # add default indexing
dft.columns = ['Date'] + list(dft.columns)[1:]      # insert 'Date' as name for date column
dft.to_csv("covidtrans.csv")

trace1 = go.Scatter(y = dft['Italy'],x = dft['Date'],mode = "lines",name = "Italy",text= "Italy")
trace2 = go.Scatter(y = dft['Spain'],x = dft['Date'],mode = "lines",name = "Spain",text= "Spain")
trace3 = go.Scatter(y = dft['Iran'], x = dft['Date'],mode = "lines",name = "Iran", text= "Iran")
data = [trace1, trace2, trace3]
layout = dict(title = 'Confirmed cases',yaxis= dict(title='Confirmed cases',ticklen=5,zeroline=False))
fig = go.Figure(data = data, layout = layout)
fig.show()
