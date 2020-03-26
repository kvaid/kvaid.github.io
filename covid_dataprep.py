import pandas as pd


input_file = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-24-2020.csv"

in_df = pd.read_csv(input_file)
in_df.rename(columns = {"Admin2":"County","Country_Region":"Country","Province_State":"State","Last_Update":"Date","Long_":"Long","Combined_Key":"Location"}, inplace = True)  # rename the columns

#in_df = in_df.drop(['state','Lat','Long'], axis=1)
#in_df = in_df.set_index('country')
#in_df = in_df.groupby('country').sum

#out_df = in_df.T                                    # Transpose
#out_df = out_df.reset_index()                             # add default indexing
#out_df.columns = ['Date'] + list(out_df.columns)[1:]      # insert 'Date' as name for date column
#out_df.to_csv("covid_groupby.csv")

print(in_df.head(10))
