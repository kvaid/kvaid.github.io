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

def plotcharts(input_df,numcountries,dropdownoption):
    data = []
    k = 0
    dft_topn = input_df.drop(['Date'],axis=1).sort_values(by=60,axis=1,ascending=False).iloc[:,0:numcountries]
    topn_countries = list(dft_topn.columns)
    dft_topn.insert(loc=0, column='Date', value=datecol) # insert 'Date' column at the beginning
    print(dft_topn,topn_countries)

    # for graphing, create the structures below dynamically
    # trace1 = go.Scatter(y = dft['Italy'],x = dft['Date'],mode = "lines",name = "Italy",text= "Italy")
    # data = [trace1, trace2, trace3, trace4]
    while k < len(topn_countries):
        temptrace = go.Scatter(y = input_df[topn_countries[k]],x = dft['Date'],mode = "lines",name = topn_countries[k],text = topn_countries[k])
        data.append(temptrace)
        k += 1

    if menuoption:
        # show menu for selecting between linear and log scales
        updatemenus = list([dict(active=1,
                                buttons=list([dict(label='Log Scale',   method='update',args=[{'title': 'Log scale',   'yaxis': {'type': 'log'}}]),
                                              dict(label='Linear Scale',method='update',args=[{'title': 'Linear scale','yaxis': {'type': 'linear'}}])
                                #buttons=list([dict(label='Log Scale',    method='update',args=[{'visible': [True, True, True, True]}, {'title': 'Log scale','yaxis': {'type': 'log'}}]),
                                #              dict(label='Linear Scale', method='update',args=[{'visible': [True, True, True, True]}, {'title': 'Linear scale','yaxis': {'type': 'linear'}}])
                                            ]),
                                )
                            ])
    else:
        updatemenus = []    # no selectable menus

    layout = dict(updatemenus=updatemenus,
                  title = 'Total cases (Confirmed minus Recovered)',
                  xaxis = dict(rangeselector=dict(buttons=list([dict(count=1, label="1m",  step="month", stepmode="backward"),
                                                                dict(count=2, label="2m",  step="month", stepmode="backward"),
                                                                dict(count=1, label="YTD", step="year",  stepmode="todate"),
                                                                dict(step="all")
                                                                ])
                                                ),
                                rangeslider=dict(visible=True),
                                ),
                  yaxis = dict(title='Confirmed cases',ticklen=5,zeroline=False))

    fig = go.Figure(data=data, layout=layout)
    fig.show()

########################################################################################################################

dfc = format_df(confirmed_filename,"covid_confirmed.csv")
datecol = dfc['Date']   # extract date column and save it for reinsertion later
del dfc['Date']         # subtracting dataframes (confirmed-recovered) requires removing 'Date' column since it is a string. we will add it back later.

dfr = format_df(recovered_filename,"covid_recovered.csv")
del dfr['Date']

dft = dfc.subtract(dfr)
dft.insert(loc=0, column='Date', value=datecol) # insert 'Date' column at the beginning
dft.to_csv("covid_total.csv")

dfd = format_df(deaths_filename,"covid_deaths.csv")
del dfd['Date']
dfd.insert(loc=0, column='Date', value=datecol) # insert 'Date' column at the beginning

# find top n countries with most cases and plot charts
plotcharts(dft,7,False)

