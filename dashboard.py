
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
ratings_users = pandas.merge(df3,df,on='user_id')

#-------------------------------------------------------------------------------

def reco_type(div_id):
	t1 = {'label': 'User-User (Collaborative-Filtering)', 'value': 1}
	t2 = {'label': 'User-Item (Content-Based)', 'value': 2}
	t3 = {'label': 'User-User + User-Item (Hybrid)', 'value': 3}
	opts = [t1, t2, t3]
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
		html.H2(children='Evaluation'),
		dcc.Graph(id='graph2'),
		#dcc.Graph(id='graph3'),

		
	], style={'width':'30%', 'display':'inline-block'}),

	html.Div(children=[
		html.H2(children='Statistic'),
		dcc.Graph(id='graph1')
		
	]),
	
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
	elif algo_value == 2:
		movie = Helper().Content_based(int(user_value))

	else:
		movie = Helper().getIdealReco(int(user_value))
	

	movie = movie[1]
	return 'Recommended Movie:  ' + movie

#-------------------------------------------------------------------------------
@app.callback(
	Output('movie-drop-p', 'children'),
	[Input('user-drop-r', 'value')],
)
def seen_movies(user_id):
	seen = list(Helper().getUserSeenMovies(int(user_id)))
	#print(seen)
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
def update_graph1(value):
	df4 = ratings_users[ratings_users.gender == 'M']  #[df3.user_id < 1000]
	df5 = ratings_users[ratings_users.gender == 'F']
	
	data0 = ratings_users.groupby(['user_id']).mean().sort_values(by=['rating'])
	data1 = df4.groupby(['user_id']).mean().sort_values(by=['rating'])
	data2 = df5.groupby(['user_id']).mean().sort_values(by=['rating'])
	return dict(
		data = [

		go.Scatter(
			x = list(range(1,6041)),
			y = data0.rating,
			mode = 'lines',
			name = 'Average user ',
		),

		go.Scatter(
			x = list(range(1,6041)),
			y = data1.rating,
			mode = 'lines',
			name = 'Male user ',
		),

		go.Scatter(
			x = list(range(1,6041)), #list(range(1,6041)),
			y = data2.rating,
			mode = 'lines',
			name = 'Female user ',
		)

		],
		layout = go.Layout(
			title = 'Average user rating distribution ',
		),
	)



#---------------------------------------------------------------------------------

@app.callback(
	Output('graph2', 'figure'),
	[Input('user-drop-r', 'value'),]
)
def update_graph2(value):

	return dict(
		data = [

		go.Bar(
			x = ['user-user', 'user-item', 'hybrid'],
			y = [0.3964575401423605, 0.48054957788445624, 0.4810461844065552],
			#mode = 'lines',
			#name = 'Average user ',
		)],
		layout = go.Layout(
			title = 'Recommendation Precision',
		),
	)


#---------------------------------------------------------------------------------
# @app.callback(
# 	Output('graph3', 'figure'),
# 	[Input('user-drop-r', 'value'),]
# )
# def update_graph3(value):

# 	return dict(
# 		data = [

# 		go.Bar(
# 			x = ['user-user', 'user-item', 'combined'],
# 			y = [0.3964575401423605, 0.48054957788445624, 0.4810461844065552],
# 			#mode = 'lines',
# 			#name = 'Average user ',
# 		)],
# 		layout = go.Layout(
# 			title = 'Recommendation Recall',
# 		),
# 	)


#---------------------------------------------------------------------------------
if __name__ == '__main__':
	app.run_server(debug=True)

	#data = df3.groupby(['user_id']).mean()
	#print(data.__dict__)
	#print(data.axes[0])



