import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import plotly.graph_objs as go

confirmed_filename = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
recovered_filename = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
deaths_filename    = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

countries_with_states = ['Australia','Canada','China','Denmark','France','Netherlands','United Kingdom','US']

<<<<<<< HEAD
# def consolidate_countries()

def format_df(input_file,output_file):
    input_df = pd.read_csv(input_file)
    input_df.rename(columns = {"Country/Region":"country","Province/State":"state"}, inplace = True)  # rename the columns
    input_df.loc[input_df['state'].notnull(),'country'] = input_df['country'] + ' ' + input_df['state'] # concat 'state' after 'country' only for columns which have non-null value for 'state'
    input_df = input_df.drop(['state','Lat','Long'], axis=1)    # delete lat, long and state columns
    input_df = input_df.set_index('country')                    # set new index to 'country' column
    output_df = input_df.T                                      # Transpose
    output_df = output_df.reset_index()                             # add back default indexing (0,1,2...n)
    output_df.columns = ['Date'] + list(output_df.columns)[1:]      # insert 'Date' as name for date column
    output_df.to_csv("filename.csv")
=======
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
>>>>>>> consolidate_country_data
    return output_df

dfc = format_df(confirmed_filename,"covid_confirmed.csv")
datecol = dfc['Date']   # extract date column and save it for reinsertion later
del dfc['Date']  # subtracting dataframes (confirmed-recovered) requires removing 'Date' column since it is a string. we will add it back later.

dfr = format_df(recovered_filename,"covid_recovered.csv")
del dfr['Date']

dft = dfc.subtract(dfr)
dft.insert(loc=0, column='Date', value=datecol) # insert 'Date' column at the beginning
print(dft)
dft.to_csv("covid_total.csv")

<<<<<<< HEAD
#dfd = format_df(deaths_filename,"covid_deaths.csv")
#del dfd['Date']
#dfd.insert(loc=0, column='Date', value=datecol) # insert 'Date' column at the beginning

=======
>>>>>>> consolidate_country_data
# find top 5 countries with most cases
#dft_index = dft.index[-1]
#dft_lastdate = dft['Date'].iloc[-1]
#print(dft_index,type(dft_index))
#print(dft_lastdate,type(dft_lastdate))

#dftlast_sorted = dft.drop(['Date'],axis=1).sort_values(by=60,axis=1,ascending=False)
#print(dftlast_sorted)


trace1 = go.Scatter(y = dft['Italy'],x = dft['Date'],mode = "lines",name = "Italy",text= "Italy")
trace2 = go.Scatter(y = dft['Spain'],x = dft['Date'],mode = "lines",name = "Spain",text= "Spain")
<<<<<<< HEAD
trace3 = go.Scatter(y = dft['Iran'], x = dft['Date'],mode = "lines",name = "Iran", text= "Iran")
trace4 = go.Scatter(y = dft['China Hubei'], x = dft['Date'],mode = "lines",name = "China", text= "China")
data = [trace1, trace2, trace3, trace4]
#layout = dict(title = 'Total outstanding cases (confirmed - recovered)',yaxis= dict(title='Total outstanding',ticklen=5,zeroline=False))
=======
trace3 = go.Scatter(y = dft['US'],   x = dft['Date'],mode = "lines",name = "US",   text= "US")
trace4 = go.Scatter(y = dft['China'],x = dft['Date'],mode = "lines",name = "China",text= "China")
data = [trace1, trace2, trace3, trace4]
# layout = dict(title = 'Total cases (Confirmed minus Recovered)',yaxis= dict(title='Confirmed cases',ticklen=5,zeroline=False))
>>>>>>> consolidate_country_data
# fig = go.Figure(data = data, layout = layout)
# fig.show()

# show menu for selecting between linear and log scales
updatemenus = list([
    dict(active=1,
         buttons=list([
            dict(label='Log Scale',
                 method='update',
<<<<<<< HEAD
                 args=[{'visible': [True, True, True]},
=======
                 args=[{'visible': [True, True, True,True]},
>>>>>>> consolidate_country_data
                       {'title': 'Log scale',
                        'yaxis': {'type': 'log'}}]),
            dict(label='Linear Scale',
                 method='update',
<<<<<<< HEAD
                 args=[{'visible': [True, True, True]},
=======
                 args=[{'visible': [True, True, True,True]},
>>>>>>> consolidate_country_data
                       {'title': 'Linear scale',
                        'yaxis': {'type': 'linear'}}])
            ]),
        )
    ])

<<<<<<< HEAD
layout = dict(updatemenus=updatemenus, title = 'Total outstanding cases (confirmed - recovered)',yaxis= dict(title='Total outstanding'))
=======
layout = dict(updatemenus=updatemenus, title = 'Total cases (Confirmed minus Recovered)',yaxis= dict(title='Confirmed cases',ticklen=5,zeroline=False))
>>>>>>> consolidate_country_data
fig = go.Figure(data=data, layout=layout)
fig.show()