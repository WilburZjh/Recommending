#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
import numpy
import nimfa
import matplotlib.pyplot as plt
from texttable import Texttable
from sklearn.decomposition import NMF

class NMF:
	def __init__(self, datafile = None):
		self.data = dict()
		for line in open(datafile):
			userid, itemid, rating,_ = line.split()
			self.data.setdefault(userid, dict())
			self.data[userid].setdefault(itemid, 0)
			self.data[userid][itemid] = int(rating)

	def shuffleData(self, k, seed, data = None, M = 8):
		random.seed(seed)

		self.traindata_matrix = numpy.zeros(shape=(943, 1682))
		self.testdata_matrix = numpy.zeros(shape=(943, 1682))

		for user, item_rating in self.data.items():
			for item, rating in item_rating.items():
				if random.randint(0, M) == k:
					self.testdata_matrix[int(user)-1][int(item)-1] = int(rating)
				else:
					self.traindata_matrix[int(user)-1][int(item)-1] = int(rating)

	def matrix_factorization(self, K, iterations=1000, alpha=0.0001, beta=0.02):
		print 'starting matrix_factorization'
		UK = numpy.random.rand(len(numpy.array(self.traindata_matrix)), K)
		KI = numpy.random.rand(K, len(numpy.array(self.traindata_matrix)[0]))
		
		for iteration in xrange(iterations):
			for i in xrange(len(self.traindata_matrix)):
				for j in xrange(len(self.traindata_matrix[i])):
					if self.traindata_matrix[i][j] > 0:
						eij = self.traindata_matrix[i][j] - numpy.dot(UK[i,:], KI[:,j])
						for k in xrange(K):
							UK[i][k] += alpha * (2 * eij * KI[k][j] - beta * UK[i][k])
							KI[k][j] += alpha * (2 * eij * UK[i][k] - beta * KI[k][j])
			e = 0
			for i in xrange(len(self.traindata_matrix)):
				for j in xrange(len(self.traindata_matrix[i])):
					if self.traindata_matrix[i][j] > 0:
						e += pow(self.traindata_matrix[i][j] - numpy.dot(UK[i,:], KI[:,j]),2)
						for k in xrange(K):
							e += (beta/2) * (pow(UK[i][k], 2) + pow(KI[k][j], 2))
			if e < 0.001:
				break

		return numpy.dot(UK, KI)

	def mae(self, k):
		snmf = numpy.array(self.matrix_factorization(k))
		self.test_matrix = numpy.zeros(shape=(943, 1682))
		result = 0
		count = 0
		for i in xrange(len(self.testdata_matrix)):
			for j in xrange(len(self.testdata_matrix[i])):
				if self.testdata_matrix[i][j] == 0:
					continue
				else:
					self.test_matrix[i][j] = snmf[i][j]
					count += 1
					result += abs(self.test_matrix[i][j]-self.testdata_matrix[i][j])
		return (result/count)
	
if __name__ == '__main__':
	nmf = NMF('/ml-100k/u.data')
	for k in [10,20,30,40,50,60,70,80]:
		for m in [1,2,3,4,5,6,7,8]:
			for seed in [40, 60, 80, 100]:
				nmf.shuffleData(m,seed)
				nmf.matrix_factorization(k)
				maerror += nmf.mae(k)
	print 'The mean absolute error is:', float(maerror/(32*8))  