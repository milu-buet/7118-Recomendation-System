'''
Goal: explore iris
1. Create a minimal Dash app with an empty graph
2. We want to let users choose which species to graph. Will create a radio items.
3. We want to let users choose attributes to plot (x and y).  Will create 2 dropdowns.
4. Minimal styling

'''
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas
from helper import Helper

#-------------------------------------------------------------------------------
df = pandas.read_csv('movielens/users.csv')

#-------------------------------------------------------------------------------

def reco_type(div_id):
	t1 = {'label': 'User-User (Collaborative-Filtering)', 'value': 1}
	t2 = {'label': 'User-Item (Content-Based)', 'value': 2}
	opts = [t1,t2,]
	return dcc.Dropdown(
		id = div_id,
		options = opts,
		value = opts[0]['value'],
	)

def user_selection(div_id):
	opts = []
	for index, row in df.iterrows():
		if row['user_id'] != 'user_id':
			opts.append( {'label':row['user_id'], 'value': row['user_id']} )
	return dcc.Dropdown(
		id = div_id,
		options = opts,
		value = opts[0]['value'],
	)

#-------------------------------------------------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
	html.H1(children='Movie Recommendation System'),
	html.Div(children='Select Algorithm'),
	html.Div([ reco_type('algo-drop') ], style={'width':'45%', 'display':'inline-block'}),
	html.Div(children='Select User'),
	html.Div([ user_selection('user-drop') ], style={'width':'45%', 'display':'inline-block'}),
	html.Div(children=''),
	html.Button('Recommend>>', id='button1'),
	html.H3(children='Recommended Movie:'),
	html.H4(id='movie',children=''),
])

#-------------------------------------------------------------------------------
@app.callback(
	Output('movie', 'children'),
	[Input('button1', 'n_clicks')],
	[
		State('algo-drop', 'value'),
		State('user-drop', 'value'),
	]
)
def rec_movie(n_clicks, algo_value, user_value):

	if algo_value == 1:
		movie = Helper().Col_filter(int(user_value))
	else:
		movie = Helper().Content_based(int(user_value))
	

	movie = movie[1]
	return html.Div(children=movie) 

#-------------------------------------------------------------------------------

if __name__ == '__main__':
	app.run_server(debug=True)



