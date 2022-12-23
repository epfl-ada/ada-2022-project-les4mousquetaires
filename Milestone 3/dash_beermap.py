from dash import Dash, dcc, html, Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import country_converter as coco
from plotly.subplots import make_subplots

cc = coco.CountryConverter()

# Import the data
df_beer_export_sim = pd.read_pickle('df_beer_export_sim.pkl') #period, user_location = f(country)
brew_country_list = pd.read_pickle('df_brew_country_list.pkl').index.to_list() # list of 204 country
beer_style_list = pd.read_pickle('df_beer_style_list.pkl').to_list() # List of 22 beer style
df_country_style = pd.read_pickle('res.pkl') # Cross tab country style
df_scaling = pd.read_pickle('df_scaling.pkl') #period, user_location = f(style)
df_damso = pd.read_pickle("the_sexiest_porthos.pkl")

df_scaling.drop('Sudan', level=1, axis=0, inplace=True) #J'enlève le Sudan ATTENTION


years = np.arange(2004,2018)#df_beer_export_sim.index.get_level_values(0).unique()[7:]
projection_types = ['natural earth', 'equirectangular', 'orthographic', 'mercator']

# Layout for the figures
layout4 = go.Layout(
    height=500, width=900,
    title='Cumulative results',
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode='x unified',

    yaxis = dict(
      gridcolor = '#909090',
      ticksuffix=' ',
      showline=True, linewidth=1, linecolor='black', mirror=True,
    ),
    xaxis = dict(
      gridcolor='#909090',
      showline=True, linewidth=1, linecolor='black', mirror=True,
      title = {'text':'year'})  
)

# Button for the projection
buttons = []
for projection_type in projection_types:
    buttons.append(dict(
                label=projection_type,
                method='relayout',
                args=[{'geo': {'projection': {'type': projection_type}}}]
                ))
    
updatemenus = list([dict(
        buttons=buttons,
        type='dropdown',
        direction='down',
        pad={'r': 10, 't': 10},
        showactive=True,
        x=0,
        xanchor='left',
        y=1.1,
        yanchor='top'
)])

''' Application Dash '''

# Display
app = Dash(__name__)
app.layout = html.Div([
    html.H2('Brewery succes simulation'),
    html.P("Select a country where you construct your brewery:"),
    dcc.Dropdown(brew_country_list, 'Switzerland', id='country-dropdown'),
    html.P("Select a type of beer that you produce in your brewery:"),
    dcc.Dropdown(beer_style_list, 'Ale', id='type-dropdown'),
    #dcc.Dropdown(projection_types, 'natural earth', id='projection-dropdown'),
    html.Div(id='output-container'),
    dcc.Graph(id="map-graph"),
    dcc.Graph(id="fig4-graph")
])

@app.callback(
    Output('map-graph', 'figure'),
    Output('fig4-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('type-dropdown', 'value'),
    #Input('projection-dropdown','value')
)
def simulation(brew_country='France', beer_type='Ale', projection='natural earth'):
    # Dataframe to store the exportation distribution in each user countries
    df_distribution = pd.DataFrame(columns=['brew_country','country', 'period', 'value'])
    
    NB_INIT_BEER = 1000
    
    beer_producted_per_year    = np.zeros(len(years)+1, int)
    beer_producted_per_year[0] = NB_INIT_BEER
    
    # Dataframe to store cumulated country where there is distributed beer (False : no distrib, True : distrib)
    country_reach_by_export = [False]*len(df_beer_export_sim.xs(2010).index) #2010 is a random id to have the size of the df
    nb_export_country       = []
    nb_cumul_beers          = []
    
    for i, year in enumerate(years):

        #D'Artagnan's part
        beer_distribution = (beer_producted_per_year[i]*df_beer_export_sim.xs(year)[brew_country]).apply(np.ceil)
        
        #Athos part
        if year == 2017:
            beer_distribution = beer_distribution.mul(df_scaling.xs(2016)[beer_type]).mul(1 + df_damso[beer_type].loc[:,2016]).fillna(0).apply(np.ceil)
        else:
            beer_distribution = beer_distribution.mul(df_scaling.xs(year)[beer_type]).mul(1 + df_damso[beer_type].loc[:,year]).fillna(0).apply(np.ceil)

        if beer_distribution.sum() == 0:
            beer_producted_per_year[i+1] = beer_producted_per_year[i]
        else:
            beer_producted_per_year[i+1] = beer_distribution.sum()
        
        if i>0:
            nb_cumul_beers.append(nb_cumul_beers[-1] + beer_distribution.sum())
        else:
            nb_cumul_beers.append(beer_distribution.sum())

        # store this data in df_distribution (beer_distribution_store just used for manipulating data)
        beer_distribution = beer_distribution.reset_index()
        beer_distribution.columns = ['country', 'distribued beer']
        beer_distribution['year'] = str(year)
        beer_distribution['brew_country'] = brew_country
        df_distribution = pd.concat([df_distribution,beer_distribution], axis=0)
        
        # Count the progression of country reached by export
        country_reach_by_export = country_reach_by_export | (beer_distribution['distribued beer'] > 0)
        nb_export_country.append(np.sum(country_reach_by_export))
        
    
    # iso_code for the graph world map
    df_distribution['iso_code'] = cc.pandas_convert(series=df_distribution.country, to='ISO3', not_found=None)
    df_distribution['happiness gauge'] = np.log10(df_distribution['distribued beer'].replace(to_replace = 0, value = 1)).round(2)
    df_distribution
    
    # Select the data for the input country, filter country with no data
    mask = (df_distribution.brew_country == brew_country) & (df_distribution['happiness gauge'] > 0)
    beer_map = px.choropleth(df_distribution[mask], locations="iso_code",
                     color="happiness gauge",
                     hover_name="country",
                     animation_frame="year",
                     title = f"Distribution brewery in {brew_country} producing {beer_type}-type beers",                 
                     color_continuous_scale=px.colors.sequential.Oranges,
                     width=900, height=700, range_color = [0, df_distribution['happiness gauge'].max()],
                     hover_data={'iso_code':False,'year':False, 'distribued beer':':.0f', 'happiness gauge':':.2f'},
                     )
    # Replace the updatemenu
    beer_map["layout"].pop("updatemenus")
    beer_map.update_layout(margin={"r":0,"t":3,"l":0,"b":0}, 
                           title={'xanchor': 'center', 'yanchor': 'top', 'y':0.98, 'x':0.5},
                           updatemenus=updatemenus)
    
    # Set the projection
    beer_map.update_geos(projection_type=projection)
    
    # fig 4
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x    = years, 
                   y    = nb_export_country,
                   line = go.scatter.Line(color='#B51F1F', width=2),
                   name = "number of country"),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x    = years, 
                   y    = nb_cumul_beers,
                   line = go.scatter.Line(color='#636EFA', width=2),
                   name = "number of produced beers"),
        secondary_y=True
    )
    
    # Set x-axis title
    fig.update_xaxes(title_text="year")

    # Set y-axes titles
    fig.update_yaxes(title_text="number of country", secondary_y=False)
    fig.update_yaxes(range = [0,np.max(nb_export_country)+2], secondary_y=False)
    fig.update_yaxes(title_text="number of beers", secondary_y=True)
    
    fig.update_layout(layout4)
    

    return beer_map, fig



if __name__ == '__main__':
    app.run_server(debug=True)