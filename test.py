import pandas as pd
import plotly.express as px

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

print(df.head())
df1 = df.melt(id_vars=['Date']+list(df.keys()[5:]), var_name='AAPL')
print(['Date']+list(df.keys()[5:]))
print(df1.head())

#fig = px.line(df1, x='Date', y='value', color='AAPL' )
#fig.show()