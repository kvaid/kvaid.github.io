import pandas as pd


input_file = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
countries_with_states = ['Australia','Canada','China','Denmark','France','Netherlands','United Kingdom','US']

input_df = pd.read_csv(input_file)
input_df.rename(columns = {"Country/Region":"country","Province/State":"state"}, inplace = True)  # rename the columns
input_df = input_df.drop(['state','Lat','Long'], axis=1)
input_df = input_df.set_index('country')
input_df = input_df.groupby('country').sum()

output_df = input_df.T                                    # Transpose
output_df = output_df.reset_index()                             # add default indexing
output_df.columns = ['Date'] + list(output_df.columns)[1:]      # insert 'Date' as name for date column
output_df.to_csv("covid_groupby.csv")
