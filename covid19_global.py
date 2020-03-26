import pandas as pd
#import matplotlib.pyplot as plt
import datetime as dt
import plotly.graph_objs as go

confirmed_cases_filename = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
#recovered_cases_filename = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
deaths_filename          = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

countries_with_states = ['Australia','Canada','China','Denmark','France','Netherlands','United Kingdom','US']

def format_df(input_file,output_file,usviews):
    in_df = pd.read_csv(input_file)
    in_df.rename(columns = {"Country/Region":"country","Province/State":"state"}, inplace = True)  # rename the columns
    #in_df.loc[in_df['state'].notnull(),'country'] = in_df['country'] + ' ' + in_df['state']
    
    in_df = in_df.loc[in_df['country']=='US']
    in_df = in_df.drop(['state','Lat','Long'], axis=1)
    in_df = in_df.set_index('country')
    in_df = in_df.groupby('country').sum()
    
    out_df = in_df.T                                          # Transpose
    out_df = out_df.reset_index()                             # add default indexing
    out_df.columns = ['Date'] + list(out_df.columns)[1:]      # insert 'Date' as name for date column
    #out_df['Date'] =  pd.to_datetime(out_df['Date'], format='%m/%d/%y') # convert 'Date' column to datefield data structure
    out_df['Date']  = out_df['Date'].apply(lambda x: dt.datetime.strptime(x,'%m/%d/%y'))
    print(out_df['Date'].head())
    out_df.to_csv("covid_groupby.csv")
    return out_df

def plotcharts(in_df,topn,dropdown):
    data = []
    k = 0
    dft_topn = in_df.drop(['Date'],axis=1).sort_values(by=60,axis=1,ascending=False).iloc[:,0:topn]
    topn_countries = list(dft_topn.columns)
    dft_topn.insert(loc=0, column='Date', value=datecol) # insert 'Date' column at the beginning
    print(dft_topn,topn_countries)

    # for graphing, create the structures below dynamically
    # trace1 = go.Scatter(y = df_global['Italy'],x = df_global['Date'],mode = "lines",name = "Italy",text= "Italy")
    # data = [trace1, trace2, trace3, trace4]
    while k < len(topn_countries):
        temptrace = go.Scatter(y = in_df[topn_countries[k]],x = df_global['Date'],mode = "lines",name = topn_countries[k],text = topn_countries[k])
        data.append(temptrace)
        k += 1

    if dropdown:
        # show menu for selecting between linear and log scales
        updatemenus = list([dict(active=1,
                                buttons=list([dict(label='Log Scale',   method='update',args=[{'title': 'Log scale',   'yaxis': {'type': 'log'}}]),
                                              dict(label='Linear Scale',method='update',args=[{'title': 'Linear scale','yaxis': {'type': 'linear'}}])]))
                                #buttons=list([dict(label='Log Scale',    method='update',args=[{'visible': [True, True, True, True]}, {'title': 'Log scale','yaxis': {'type': 'log'}}]),
                                #              dict(label='Linear Scale', method='update',args=[{'visible': [True, True, True, True]}, {'title': 'Linear scale','yaxis': {'type': 'linear'}}])
                            ])
    else:
        updatemenus = []    # no selectable menus

    layout = dict(updatemenus=updatemenus,
                  title = 'Total cases (Confirmed minus Recovered)',
                  xaxis = dict(rangeselector=dict(buttons=list([dict(count=1, label="1m",  step="month", stepmode="backward"),
                                                                dict(count=2, label="2m",  step="month", stepmode="backward"),
                                                                dict(count=1, label="YTD", step="year",  stepmode="todate"),
                                                                dict(step="all")
                                                                ])),
                                rangeslider=dict(visible=True),type="date"),
                  yaxis = dict(title='Total cases',ticklen=5,zeroline=False))

    fig = go.Figure(data=data, layout=layout)
    fig.show()

########################################################################################################################

dfc_global = format_df(confirmed_cases_filename,"covid_confirmed_global.csv",usviews=False)
datecol = dfc_global['Date']   # extract date column and save it for reinsertion later
del dfc_global['Date']         # subtracting dataframes (confirmed-recovered) requires removing 'Date' column since it is a string. we will add it back later.

#dfr = format_df(recovered_cases_filename,"covid_recovered.csv")
#del dfr['Date']

dfd_global = format_df(deaths_filename,"covid_deaths_global.csv",usviews=False)
del dfd_global['Date']

#df_global = dfc.subtract(dfr)     # Total = Confirmed - Recovered - Deaths
df_global = dfc_global.subtract(dfd_global)
df_global.insert(loc=0, column='Date', value=datecol) # insert 'Date' column at the beginning
df_global.to_csv("covid_global.csv")
dfd_global.insert(loc=0, column='Date', value=datecol) # insert 'Date' column at the beginning

# find top n countries with most cases and plot charts
plotcharts(df_global,topn=7,dropdown=False)

