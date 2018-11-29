

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import random
from helper import Helper
import pandas

import time
ratings_file = 'movielens/ratings.csv'
qid=0
userId = 611
movie = 'Toy Story (1995)'
movieId = 1

tp=0
fp=0

def addnewRating(userId, movieId, rating):
    global tp,fp

    if float(rating) >= 3.5:
        tp+=1
    else: fp+=1

    timestamp = int(time.time())
    df = pandas.read_csv(ratings_file)
    a = df[(df.user_id == userId) & (df.movie_id == movieId)]
    if len(a) < 1:
        df = df.append({'user_id' : userId , 'movie_id' : movieId, 'rating': rating, 'timestamp': timestamp} , ignore_index=True)
        df.to_csv(ratings_file, index=False)

def getRandomUnseenMovie(userId):
    a = Helper().getRandomUnseenMovie(userId)
    #print(a)
    return a


def getRecommendedMovie(userId): 
    return Helper().Col_filter(userId)


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




def create_app():

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.config['suppress_callback_exceptions']=True
    setAppLayout(app)
    app.run_server(debug=True)


def getLayout(options):

    return html.Div(children=[
            html.H1(children = "New User Evaluation"),
            html.Div(children='Select Algorithm'),
            html.Div([ reco_type('algo-drop') ], style={'width':'45%', 'display':'inline-block'}),
            html.H2(id='head', children='Q'+ str(options['qid'])+'. Rate this movie'),
            html.Div(children='Name: ' + options['movie']),
            'Rating: ',
            dcc.Input(
                id='input-box',
                placeholder='Enter ratings...',
                type='text',
                value=''
            ),
            html.Div(id='dum', children=''),
            html.Button('Submit', id='button1')

        ])

def getWelcomeLayout():
    
    return html.Div(children=[
            html.H1(id='head', children='Loading ....'),
            dcc.Input(
                id='input-box',
                placeholder='Enter ratings...',
                type='text',
                value='',
            ),
            html.Div(id='dum', children=''),
            html.Button('Submit', id='button1')

        ])

def getEndLayout():
    precision = float(tp) / (tp + fp)
    return html.H1(children="Precision:" + str(precision))



def setAppLayout(app):

    options = {'qid':0, 'movie':'movie'}
    app.layout = html.Div(id ='page-content',children=getWelcomeLayout())

    @app.callback(
    Output(component_id='page-content', component_property='children'),
    [Input('button1', 'n_clicks')],
    [
        #State('algo-drop', 'value'),
        State('input-box', 'value'),
        

    ]
    )
    def rate(n_clicks, value):
        global qid, userId, movie, movieId
        algo = 1

        if qid == 5:
            return getEndLayout()

        if qid > 0 and qid < 6:
            addnewRating(userId, movieId, value)

        if qid == 0:
            movieId, movie = getRandomUnseenMovie(userId)
        else:
            if algo == 1:
                movieId, movie = Helper().Col_filter(userId)
            elif algo == 2:
                movieId, movie = Helper().Content_based(userId)
            else:
                movieId, movie = Helper().getIdealReco(userId)

        
        qid += 1
        options = {'qid':qid, 'movie':movie}
        return getLayout(options)

if __name__ == '__main__':
    create_app()
    #addnewRating(611, 170875, 3)