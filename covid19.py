import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
#import plotly.express as px
import plotly.graph_objs as go

df = pd.read_csv("covid19.csv")
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

# Creating trace1
# trace1 = go.Scatter(x = dft['Italy '],
#                     y = dft['Date'],
#                     mode = "lines",
#                     name = "Italy",
#                     marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
#                     text= "Italy")
# # Creating trace2
# trace2 = go.Scatter(
#                     x = dft['Spain '],
#                     y = dft['Date'],
#                     mode = "lines",
#                     name = "Spain",
#                     marker = dict(color = 'rgba(80, 26, 80, 0.8)'),
#                     text= "Spain")
# data = [trace1, trace2]
# layout = dict(title = 'Confirmed cases',
#               xaxis= dict(title= 'Confirmed',ticklen= 5,zeroline= False)
#              )
# fig = dict(data = data, layout = layout)
