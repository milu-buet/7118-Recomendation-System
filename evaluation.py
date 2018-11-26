# Md Lutfar Rahman
# mrahman9@memphis.edu

from matrix import Matrix
import numpy
import random
import pandas
ratings_file = 'movielens/ratings.csv'
movie_file = 'movielens/movies.csv'
no_users = 6041
no_movies = 3953
from helper import Helper


class Evaluation(object):
	"""docstring for Evaluation"""
	def __init__(self):
		self.movie_df = pandas.read_csv(movie_file)
		self.rating_df = pandas.read_csv(ratings_file)
		self.avg_rating = self.rating_df.groupby(['user_id']).mean()


	
	# def singleUserTest(self, userId):
	# 	df = self.rating_df[self.rating_df.user_id == userId]
	# 	df = df[df.rating == df.rating.max()].movie_id

	# 	#print(df)

	# 	for a_movie in list(df):
	# 		#a_movie =  random.choice(list(df))

	# 		new_df = self.rating_df[self.rating_df.movie_id != a_movie]
	# 		h = Helper(new_df) 

	# 		M = 40
	# 		A = h.getRecommendedMovieCol(userId, M)
	# 		B = list(h.getRecommendedMovieCont(userId, M))
	# 		C = list(h.getIdealRecos(userId, M))

	# 		#print(a_movie,A,B,C)
	# 		results = a_movie in A, a_movie in B, a_movie in C
	# 		print(results)

	# 	return results

	def singleUserTest2(self, h, userId):

		user_avg = self.avg_rating.rating[userId]

		#print(user_avg)

		
		A = h.Col_filter(userId)[0]
		B = h.Content_based(userId)[0]
		C = h.getIdealReco(userId)[0]

		if self.getApproxRating(h, A, userId) > user_avg and self.getApproxRating(h, A, userId) > 3.5:
			A = 1
		else: A = 0

		if self.getApproxRating(h, B, userId) > user_avg and self.getApproxRating(h, B, userId) > 3.5:
			B = 1
		else: B =  0

		if self.getApproxRating(h, C, userId) > user_avg and self.getApproxRating(h, C, userId) > 3.5:
			C = 1
		else: C = 0	

		#print(A,B,C)

		return A,B,C


	def allUserTest(self):
		
		A,B,C = 0,0,0
		h = Helper()
		for user in range(1,no_users):
			print(user)
			a,b,c = self.singleUserTest2(h, user)
			A += a
			B += b 
			C += c 


		A = float(A)/no_users
		B = float(B)/no_users
		C = float(C)/no_users

		return A,B,C   # precision for three algorithm



	def getApproxRating(self, h, movieId, userId):

		if movieId is None:
			return 0

		genres = h.Movies[movieId][1].split('|') #self.getMovieGenres(movieId)


		rate_sum = 0
		for feature in genres:

			if feature in h.feature_rate[userId]:
				rate_sum += h.feature_rate[userId][feature][0]

		return rate_sum/len(genres)
	

	def getMovieGenres(self, movieId):
		sr = self.movie_df[self.movie_df.movie_id == movieId]
		sr = list(sr.genres)[0].split('|')
		return sr





if __name__== "__main__":
	E = Evaluation()
	#print(E.singleUserTest2(611))
	print(E.allUserTest())