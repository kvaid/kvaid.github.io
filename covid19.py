import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import plotly.graph_objs as go

def format_df(input_df,filename):
    input_df.rename(columns = {"Country/Region":"country","Province/State":"state"}, inplace = True)  # rename the columns
    input_df.loc[input_df['state'].notnull(),'country'] = input_df['country'] + ' ' + input_df['state']
    input_df = input_df.drop(['state','Lat','Long'], axis=1)
    input_df = input_df.set_index('country')
    dft = input_df.T                                    # Transpose
    dft = dft.reset_index()                             # add default indexing
    dft.columns = ['Date'] + list(dft.columns)[1:]      # insert 'Date' as name for date column
    dft.to_csv("filename")
    return dft


dfc = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
dfr = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv")

# dfc.rename(columns = {"Country/Region":"country","Province/State":"state"}, inplace = True)  # rename the columns
# dfc.loc[dfc['state'].notnull(),'country'] = dfc['country'] + ' ' + dfc['state']
# dfc = dfc.drop(['state','Lat','Long'], axis=1)
# dfc = dfc.set_index('country')
# dfct = dfc.T                                          # Transpose
# dfct = dfct.reset_index()                             # add default indexing
# dfct.columns = ['Date'] + list(dfct.columns)[1:]      # insert 'Date' as name for date column
# dfct.to_csv("covid_confirmed.csv")

# dfr.rename(columns = {"Country/Region":"country","Province/State":"state"}, inplace = True)  # rename the columns
# dfr.loc[dfr['state'].notnull(),'country'] = dfr['country'] + ' ' + dfr['state']
# dfr = dfr.drop(['state','Lat','Long'], axis=1)
# dfr = dfr.set_index('country')
# dfrt = dfr.T                                          # Transpose
# dfrt = dfrt.reset_index()                             # add default indexing
# dfrt.columns = ['Date'] + list(dfrt.columns)[1:]      # insert 'Date' as name for date column
# dfrt.to_csv("covid_recovered.csv")

dfct = format_df(dfc,"covid_confirmed.csv")
dfrt = format_df(dfr,"covid_recovered.csv")
df_datecol = dfct['Date']   # extract date column and save it for reinsertion later
del dfct['Date']
del dfrt['Date']
df = dfct.subtract(dfrt)
print(df)
df.to_csv("covid_total.csv")

# find top 5 countries with most cases
#dft_index = dft.index[-1]
#dft_lastdate = dft['Date'].iloc[-1]
#print(dft_index,type(dft_index))
#print(dft_lastdate,type(dft_lastdate))

#dftlast_sorted = dft.drop(['Date'],axis=1).sort_values(by=60,axis=1,ascending=False)
#print(dftlast_sorted)


# trace1 = go.Scatter(y = dft['Italy'],x = dft['Date'],mode = "lines",name = "Italy",text= "Italy")
# trace2 = go.Scatter(y = dft['Spain'],x = dft['Date'],mode = "lines",name = "Spain",text= "Spain")
# trace3 = go.Scatter(y = dft['Iran'], x = dft['Date'],mode = "lines",name = "Iran", text= "Iran")
# data = [trace1, trace2, trace3]
# layout = dict(title = 'Confirmed cases',yaxis= dict(title='Confirmed cases',ticklen=5,zeroline=False))
# fig = go.Figure(data = data, layout = layout)
# fig.show()

# # show menu for selecting between linear and log scales
# updatemenus = list([
#     dict(active=1,
#          buttons=list([
#             dict(label='Log Scale',
#                  method='update',
#                  args=[{'visible': [True, True, True]},
#                        {'title': 'Log scale',
#                         'yaxis': {'type': 'log'}}]),
#             dict(label='Linear Scale',
#                  method='update',
#                  args=[{'visible': [True, True, True]},
#                        {'title': 'Linear scale',
#                         'yaxis': {'type': 'linear'}}])
#             ]),
#         )
#     ])

# layout = dict(updatemenus=updatemenus, title='Linear scale')
# fig = go.Figure(data=data, layout=layout)
# fig.show()