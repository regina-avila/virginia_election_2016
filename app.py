######### Import your libraries #######
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *


###### Import a dataframe #######

df0 = pd.read_csv('Virginia.csv')
df1=df0[['county_name', 'jurisdiction', 'precinct', 'candidate', 'votes']]
df1.loc[(df1['candidate']!='Hillary Clinton') & (df1['candidate']!='Donald Trump'), 'candidate']='Other'
df2=df1.groupby(['county_name', 'jurisdiction', 'precinct', 'candidate']).sum()
df3=df2.unstack(level=-1)
df4=df3.reset_index()
options_list=list(df4['jurisdiction'].value_counts().sort_index().index)
####### Set up your app #####
app = dash.Dash(__name__)
server = app.server
app.title='VA 2016'
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


####### Layout of the app ########
app.layout = html.Div([
    html.H3('2016 Presidential Election: Vote Totals by Jurisdiction'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in options_list],
        value=options_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.Br(),
    html.A('Code on Github', href='https://github.com/austinlasseter/virginia_election_2016'),
])


######### Interactive callbacks go here #########
@app.callback(dash.dependencies.Output('display-value', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def juris_picker(juris_name):
    juris_df=df4[df4['jurisdiction']==juris_name]

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


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
