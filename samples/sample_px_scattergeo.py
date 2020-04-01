import plotly.express as px

df = px.data.gapminder()
print(df.head())

# all parameters at https://plotly.com/python-api-reference/generated/plotly.express.scatter_geo.html
fig = px.scatter_geo(df,
        title='world map with data',
        projection='natural earth', # 'orthographic','natural earth','equirectangular','albers usa'locations='iso_alpha', # column name with location type info
        locationmode='ISO-3', # ‘ISO-3’,‘USA-states’,‘country names’ 
        locations='iso_alpha', # column with location information
        scope='world', # 'world','usa','europe','asia','africa','north america','south america'
        color='continent', # which column to use to set the color of markers for scatter bubbles
        size='pop', # size of markers, "pop" is one of the columns of gapminder
        hover_name='country', # first row shown in hover box, should be column of dataframe
        text='lifeExp', # column name to add to hover box data
        animation_frame='year', # column name to show range of animation frame
        animation_group='country', # column name that is constant across animation_frame data
        )
fig.show()

#plotly.offline.plot(fig,filename='/plotly_offline_plot.html',auto_open=False)