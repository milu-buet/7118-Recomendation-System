import numpy

class Matrix:
	def __init__(self, name, rows, cols):
		self.name = name
		self.rows = rows
		self.cols = cols
		self.mat = numpy.zeros([len(rows), len(cols)])

	def set(self, row_i, value):
		self.mat[row_i] = value

	def show(self):
		W = 15
		print(self.name)
		print(' '*W, end='')
		for c in self.cols:
			print(' '*(W-len(c)), end='')
			print(c, end='')
		print()
		for i, r in enumerate(self.rows):
			#print(self.row)
			print(self.rows[i], end='')
			print(' '*(W-len(str(self.rows[i]))), end='')
			for j in range(len(self.cols)):
				print('{:10.1f}'.format(self.mat[i][j]), end='\t')
			print()
		print()
