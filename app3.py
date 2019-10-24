######### Import your libraries #######
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *
import numpy as np

###### Import a dataframe #######
df = pd.read_pickle('virginia_totals.pkl')
options_list=list(df['jurisdiction'].value_counts().sort_index().index)

# Read in the USA counties shape files
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='VA 2016'

####### Layout of the app ########
app.layout = html.Div([
    html.H3('2016 Presidential Election: Vote Totals by Jurisdiction'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in options_list],
        value=options_list[10]
    ),
    html.Br(),
    dcc.Graph(id='display-map'),
    dcc.Graph(id='display-value'),
    html.Br(),
    html.A('Code on Github', href='https://github.com/austinlasseter/virginia_election_2016'),
    html.Br(),
    html.A('Data Source', href='https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LYWX3D')
])


######### Callback #1 #########
@app.callback(dash.dependencies.Output('display-value', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def juris_picker(juris_name):
    juris_df=df[df['jurisdiction']==juris_name]

    mydata1 = go.Bar(x=list(juris_df['precinct'].value_counts().index),
                     y=list(juris_df['votes']['Donald Trump']),
                     marker=dict(color='#122A7F'),
                     name='Trump')
    mydata2 = go.Bar(x=list(juris_df['precinct'].value_counts().index),
                     y=list(juris_df['votes']['Hillary Clinton']),
                     marker=dict(color='#f96800'),
                     name='Clinton')
    mydata3 = go.Bar(x=list(juris_df['precinct'].value_counts().index),
                     y=list(juris_df['votes']['Other']),
                     marker=dict(color='#009900'),
                     name='Other')

    mylayout = go.Layout(
        title='Votes by candidate for: {}'.format(juris_name),
        xaxis=dict(title='Precincts'),
        yaxis=dict(title='Number of Votes')
    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig



######### Callback #2 #########
@app.callback(dash.dependencies.Output('display-map', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def juris_highlighter(juris_name):
    df['selected']=np.where(df['jurisdiction']==juris_name, 1, 0)
    fig = go.Figure(go.Choroplethmapbox(geojson=counties,
                                        locations=df['FIPS'],
                                        z=df['selected'],
                                        # colorscale=['blues'],
                                        text=df['county_name'],
                                        hoverinfo='text',
                                        zmin=0,
                                        zmax=1,
                                        marker_line_width=.5
                                        ))
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=5.8,
                      mapbox_center = {"lat": 38.0293, "lon": -79.4428})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig



######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
