# Md Lutfar Rahman
# mrahman9@memphis.edu



from matrix import Matrix
import numpy
import random
ratings_file = 'movielens/ratings.csv'
movie_file = 'movielens/movies.csv'
no_users = 6041
no_movies = 3953


# Reads data, runs the main algorithm
class Helper(object):
	"""docstring for Helper"""
	def __init__(self):
		self.getMovieData()
		self.getRatingData()
		


	def getMovieData(self):
		self.Movies = {}
		self.features = set()
		f = open(movie_file)
		f.readline()

		for line in f:
			ll = line.strip().split(',')
			movieId = int(ll[0])
			genres = ll[-1]
			movieName = line[len(ll[0])+1:-len(genres)-2]
			movieName = movieName.replace('"','')

			self.Movies[movieId] = (movieName,genres)
			

			nfeatures = genres.split('|')
			self.features |= set(nfeatures)

		self.features = sorted(list(self.features))


	def getRatingData(self):
		self.Ratings = {}
		self.feature_rate = {}
		self.userseen = {}
		f = open(ratings_file)
		f.readline()

		for line in f:
			userId,movieId,rating,timestamp = line.strip().split(',')

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

				if userId not in self.userseen:
					self.userseen[userId] = []

				self.userseen[userId].append(movieId)


	def getunseenmovies(self, userId):

		if userId in self.userseen:
			seen = set(self.userseen[userId])
		else:
			seen = set()
			
		unseen = set(self.Movies.keys()) - seen

		return unseen


	def getRandomUnseenMovie(self, userId):
		items = list(self.getunseenmovies(userId))
		a_movie =  random.choice(items)
		#print(a_movie)
		return a_movie, self.Movies[a_movie][0] 
			
		

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



	def getRecommendedMovie(self, userId):
		self.UF = self.getUserFeature()
		UU = numpy.matmul(self.UF.mat, numpy.transpose(self.UF.mat))
		user_user = list(UU[userId])
		user_user[userId] = 0
		#print(user_user)
		close_user = user_user.index(max(user_user))
		recommended_movies = self.getunseenmovies(userId).intersection(set(self.userseen[close_user]))

		a_movie = list(recommended_movies)[0]
		#print(a_movie)

		return a_movie, self.Movies[a_movie][0]



	def Col_filter(self, userId):
		return self.getRecommendedMovie(userId)

	def Content_based(self, userId):
		self.UF = self.getUserFeature()
		self.IF = self.getItemFeature()

		UI = numpy.matmul(self.UF.mat, numpy.transpose(self.IF.mat))
		#recommended_movies = self.getunseenmovies(userId).intersection(set(self.userseen[close_user]))


		for seen in self.userseen[userId]:
			UI[userId][seen] = 0


		a_movie = numpy.argmax(UI[userId])

		return a_movie, self.Movies[a_movie][0]





if __name__== "__main__":
	a = Helper()
	#UF = a.UF
	#print(UF.show())
	
	#print(list(UI[610]).index(max(UI[610])))

	#print(a.getRecommendedMovie(611) )

	print(a.Content_based(611))
	#print(a.IF.show())