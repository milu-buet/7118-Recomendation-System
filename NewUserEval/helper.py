# Md Lutfar Rahman
# mrahman9@memphis.edu



from matrix import Matrix
import numpy
import random
import pandas
ratings_file = 'movielens/ratings.csv'
movie_file = 'movielens/movies.csv'
no_users = 6042
no_movies = 3953


# Reads data, runs the main algorithm
class Helper(object):
	"""docstring for Helper"""
	def __init__(self, rating_df = pandas.DataFrame()):

	
		self.movie_df = pandas.read_csv(movie_file)
		

		if not rating_df.empty:
			self.rating_df = rating_df #pandas.read_csv('movielens/ratings.csv')
		else:
			self.rating_df = pandas.read_csv(ratings_file)
		
		self.getMovieData()
		self.getRatingData()
		self.UF = self.getUserFeature()
		self.IF = self.getItemFeature()
		self.UU = numpy.matmul(self.UF.mat, numpy.transpose(self.UF.mat))
		self.UI = numpy.matmul(self.UF.mat, numpy.transpose(self.IF.mat))
		


	def getMovieData(self):
		self.Movies = {}
		self.features = set()

		
		#f = open(movie_file)
		#f.readline()

		for index, row in self.movie_df.iterrows():
		#for line in f:
			#ll = line.strip().split(',')
			movieId = int(row['movie_id']) #int(ll[0])
			genres = row['genres']#ll[-1]
			movieName = row['title']#line[len(ll[0])+1:-len(genres)-2]
			movieName = movieName.replace('"','')

			self.Movies[movieId] = (movieName,genres)
			

			nfeatures = genres.split('|')
			self.features |= set(nfeatures)

		self.features = sorted(list(self.features))


	def getMovieGenres(self, movieId):
		sr = self.movie_df[self.movie_df.movie_id == movieId]
		sr = list(sr.genres)[0].split('|')
		return sr

	def getMovieTitle(self, movieId):
		sr = self.movie_df[self.movie_df.movie_id == movieId]
		sr = list(sr.title)[0]
		return sr


	def getRating(self, userId, movieId):
		pass


	def getUserSeenMovies(self, userId):

		sr = self.rating_df[self.rating_df.user_id == userId].movie_id
		#print(set(sr))
		return set(sr)

	def getUserUnseenMovies(self, userId):
		
		sr = set(self.movie_df.movie_id)
		return sr - self.getUserSeenMovies(userId)


	def getRatingData(self):
		self.Ratings = {}
		self.feature_rate = {}

		self.rating_df.to_csv('movielens/dum.csv', index=False)

		f = open('movielens/dum.csv')
		f.readline()

		for line in f:
		#for index, row in df3.iterrows():

			userId,movieId,rating,timestamp = line.strip().split(',')#row['user_id'], row['movie_id'], row['rating'], row['timestamp'] #

			userId = int(userId)
			movieId = int(movieId)
			

			if userId not in self.Ratings:
				self.Ratings[userId] = {}

			if len(rating) > 0:
				rating = float(rating)
				self.Ratings[userId][movieId] = rating

				if userId not in self.feature_rate:
					self.feature_rate[userId] = {}

				for genre in self.Movies[movieId][1].split('|'):
					if genre not in self.feature_rate[userId]:
						self.feature_rate[userId][genre] = (0,0,0)
					b,c = self.feature_rate[userId][genre][1] + rating, self.feature_rate[userId][genre][2]+1
					a = round(b/c,2)
					self.feature_rate[userId][genre] = (a,b,c)


	def getRandomUnseenMovie(self, userId):
		items = list(self.getUserUnseenMovies(userId))
		a_movie =  random.choice(items)
		return a_movie, self.getMovieTitle(a_movie) 
			
		

	def getUserFeature(self):
		UF = Matrix(
			'UserFeature',
			list(range(no_users)), 
			self.features
		)

		for userId in range(no_users):
			row = []
			for feature in self.features:
				if userId in self.feature_rate and feature in self.feature_rate[userId]:
					row.append(self.feature_rate[userId][feature][0])
				else:
					row.append(0)

			#print(row)
			UF.set(userId, row)


		return UF

	def getItemFeature(self):
		IF = Matrix(
			'ItemFeature',
			list(range(no_movies)), 
			self.features
		)

		for movieId in range(no_movies):
			row = []
			for feature in self.features:
				if movieId in self.Movies and feature in self.Movies[movieId][1]:
					row.append(1)
				else:
					row.append(0)

			#print(row)
			IF.set(movieId, row)


		return IF



	def getRecommendedMovieCol(self, userId, M=10):
		#self.UF = self.getUserFeature()
		#UU = numpy.matmul(self.UF.mat, numpy.transpose(self.UF.mat))
		user_user = list(self.UU[userId])
		user_user[userId] = 0
		#print(user_user)
		close_user = user_user.index(max(user_user))
		recommended_movies = self.getUserUnseenMovies(userId).intersection(self.getUserSeenMovies(close_user))

		return list(recommended_movies)[0:M]
		#print(a_movie)

		#return a_movie, self.Movies[a_movie][0]



	def Col_filter(self, userId):
		a_movie = self.getRecommendedMovieCol(userId)[0]
		return a_movie, self.Movies[a_movie][0]

	def getRecommendedMovieCont(self, userId, M=10):
		#self.UF = self.getUserFeature()
		#self.IF = self.getItemFeature()

		#UI = numpy.matmul(self.UF.mat, numpy.transpose(self.IF.mat))
		UI = self.UI.copy()
		for seen in self.getUserSeenMovies(userId):
			UI[userId][seen] = 0

		recs = []

		for i in range(M):
			a_movie = numpy.argmax(UI[userId])
			UI[userId][a_movie] = 0
			recs.append(a_movie)

		return recs
	

	def Content_based(self, userId):
		# self.UF = self.getUserFeature()
		# self.IF = self.getItemFeature()

		# UI = numpy.matmul(self.UF.mat, numpy.transpose(self.IF.mat))
		# #recommended_movies = self.getunseenmovies(userId).intersection(set(self.userseen[close_user]))


		# for seen in self.getUserSeenMovies(userId):
		# 	UI[userId][seen] = 0


		a_movie = self.getRecommendedMovieCont(userId)[0]

		return a_movie, self.Movies[a_movie][0]



	def getIdealRecos(self,userId, M = 30):

		#M = 20
		A = set(self.getRecommendedMovieCol(userId, M))
		B = set(self.getRecommendedMovieCont(userId, M))

		return A.intersection(B)


	def getIdealReco(self,userId):

		recos = list(self.getIdealRecos(userId))

		if recos == []:
			return None, None

		a_movie = recos[0]
		return a_movie, self.Movies[a_movie][0]







if __name__== "__main__":
	a = Helper()
	#UF = a.UF
	#print(UF.show())
	
	#print(list(UI[610]).index(max(UI[610])))

	#print(a.getRecommendedMovieCol(611) )
	#print(a.getRecommendedMovieCont(611) )

	print(a.getIdealRecos(700,30))

	#print(a.Content_based(611))
	#print(a.IF.show())

	#print(a.getRandomUnseenMovie(611))

	#print(a.getMovieTitle(1))

	#print(a.getUserUnseenMovies(611))