import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import plotly.graph_objs as go

confirmed_filename = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
recovered_filename = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
deaths_filename    = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

countries_with_states = ['Australia','Canada','China','Denmark','France','Netherlands','United Kingdom','US']

def format_df(input_file,output_file):
    input_df = pd.read_csv(input_file)
    input_df.rename(columns = {"Country/Region":"country","Province/State":"state"}, inplace = True)  # rename the columns
    #input_df.loc[input_df['state'].notnull(),'country'] = input_df['country'] + ' ' + input_df['state']
    input_df = input_df.drop(['state','Lat','Long'], axis=1)
    input_df = input_df.set_index('country')
    input_df = input_df.groupby('country').sum()
    output_df = input_df.T                                    # Transpose
    output_df = output_df.reset_index()                             # add default indexing
    output_df.columns = ['Date'] + list(output_df.columns)[1:]      # insert 'Date' as name for date column
    output_df.to_csv("covid_groupby.csv")
    return output_df

dfc = format_df(confirmed_filename,"covid_confirmed.csv")
dfr = format_df(recovered_filename,"covid_recovered.csv")
dfd = format_df(deaths_filename,   "covid_deaths.csv")
datecol = dfc['Date']   # extract date column and save it for reinsertion later
del dfc['Date']
del dfr['Date']
del dfd['Date']
dft = dfc.subtract(dfr)
dft.insert(loc=0, column='Date', value=datecol) # insert 'Date' column at the beginning
dfd.insert(loc=0, column='Date', value=datecol) # insert 'Date' column at the beginning
print(dft)
dft.to_csv("covid_total.csv")

# find top 5 countries with most cases
#dft_index = dft.index[-1]
#dft_lastdate = dft['Date'].iloc[-1]
#print(dft_index,type(dft_index))
#print(dft_lastdate,type(dft_lastdate))

#dftlast_sorted = dft.drop(['Date'],axis=1).sort_values(by=60,axis=1,ascending=False)
#print(dftlast_sorted)


trace1 = go.Scatter(y = dft['Italy'],x = dft['Date'],mode = "lines",name = "Italy",text= "Italy")
trace2 = go.Scatter(y = dft['Spain'],x = dft['Date'],mode = "lines",name = "Spain",text= "Spain")
trace3 = go.Scatter(y = dft['US'],   x = dft['Date'],mode = "lines",name = "US",   text= "US")
trace4 = go.Scatter(y = dft['China'],x = dft['Date'],mode = "lines",name = "China",text= "China")
data = [trace1, trace2, trace3, trace4]
# layout = dict(title = 'Total cases (Confirmed minus Recovered)',yaxis= dict(title='Confirmed cases',ticklen=5,zeroline=False))
# fig = go.Figure(data = data, layout = layout)
# fig.show()

# show menu for selecting between linear and log scales
updatemenus = list([
    dict(active=1,
         buttons=list([
            dict(label='Log Scale',
                 method='update',
                 args=[{'visible': [True, True, True,True]},
                       {'title': 'Log scale',
                        'yaxis': {'type': 'log'}}]),
            dict(label='Linear Scale',
                 method='update',
                 args=[{'visible': [True, True, True,True]},
                       {'title': 'Linear scale',
                        'yaxis': {'type': 'linear'}}])
            ]),
        )
    ])

layout = dict(updatemenus=updatemenus, title = 'Total cases (Confirmed minus Recovered)',yaxis= dict(title='Confirmed cases',ticklen=5,zeroline=False))
fig = go.Figure(data=data, layout=layout)
fig.show()