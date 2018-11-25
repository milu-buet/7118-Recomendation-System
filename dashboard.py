
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas
from helper import Helper

#-------------------------------------------------------------------------------
ratings_file = 'movielens/ratings.csv'
df = pandas.read_csv('movielens/users.csv')
df2 = pandas.read_csv('movielens/movies.csv')
df3 = pandas.read_csv(ratings_file)

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

def get_movie_opts(seen=[]):
	opts = []
	for index, row in df2.iterrows():
		if row['movie_id'] != 'movie_id' and row['movie_id'] not in seen:
			opts.append( {'label':row['title'], 'value': row['movie_id']} )

	return opts

def movie_selection(div_id, seen=[]):
	opts = get_movie_opts(seen)
	return dcc.Dropdown(
		id = div_id,
		options = opts,
		value = opts[0]['value'],
	)

import time
 
def addnewRating(userId, movieId, rating):
    timestamp = int(time.time())
    a = df3[(df3.user_id == userId) & (df3.movie_id == movieId)]
    if len(a) < 1:
        df4 = df3.append({'user_id' : userId , 'movie_id' : movieId, 'rating': rating, 'timestamp': timestamp} , ignore_index=True)
        df4.to_csv(ratings_file, index=False)

#-------------------------------------------------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
	html.H1(children='Movie Recommendation System', style={'text-align':'center'}),
	html.Div(children=[
		html.H2(children='Recommendation System'),
		html.Div(children='Select Algorithm'),
		html.Div([ reco_type('algo-drop') ], style={'width':'45%', 'display':'inline-block'}),
		html.Div(children='Select User'),
		html.Div([ user_selection('user-drop') ], style={'width':'45%', 'display':'inline-block'}),
		html.Div(children=''),
		html.Button('Recommend', id='button1'),
		html.H5(id='movie', children='Recommended Movie:'),
	]),

	html.Div(children="\n\n"),

	html.Div(children=[
		html.H2(children='Add Rating'),
		html.Div(children='Select User'),
		html.Div([ user_selection('user-drop-r') ], style={'width':'45%', 'display':'inline-block'}),
		html.Div(children='Select Movie'),
		html.Div(id = 'movie-drop-p' ,children = [ movie_selection('movie-drop-r') ], style={'width':'45%', 'display':'inline-block'}),
		html.Div(children='Rating'),
		dcc.Input(
                id='input-box',
                placeholder='Enter rating...',
                type='text',
                value=''
            ),
		html.Div(id='dum', children=''),
        html.Button('Submit', id='button2')
	]),

	html.Div(children=[
		html.H2(children='Statistic'),
		dcc.Graph(id='graph1')
		
	]),

	html.Div(children=[
		html.H2(children='Evaluation'),
		
	])
	
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
	return 'Recommended Movie:  ' + movie

#-------------------------------------------------------------------------------
@app.callback(
	Output('movie-drop-p', 'children'),
	[Input('user-drop-r', 'value')],
)
def seen_movies(user_id):
	seen = Helper().userseen[int(user_id)]     
	return [movie_selection('movie-drop-r',seen)]
#---------------------------------------------------------------------------------
@app.callback(
	Output('dum', 'children'),
	[Input('button2', 'n_clicks')],
	[
		State('user-drop-r', 'value'),
		State('movie-drop-r', 'value'),
		State('input-box', 'value')
	]
)
def rate(n_clicks, user_id, movie_id, rating):
	if n_clicks:
		addnewRating(user_id, movie_id, rating)

	return ""
#---------------------------------------------------------------------------------
@app.callback(
	Output('graph1', 'figure'),
	[Input('user-drop-r', 'value'),]
)
def update_graph(species_name):
	df4 = df3[df3.user_id < 200]
	data = df4.groupby(['user_id']).mean()
	return dict(
		data = [go.Scatter(
			x = data.axes[0],
			y = data.rating,
			mode = 'lines',
			name = 'user rating',
		)],
		layout = go.Layout(
			title = 'User Rating',
		),
	)



#---------------------------------------------------------------------------------

if __name__ == '__main__':
	app.run_server(debug=True)

	#data = df3.groupby(['user_id']).mean()
	#print(data.__dict__)
	#print(data.axes[0])



