#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
import numpy

def matrix_factorization(R, P, Q, K, iterations=5000, alpha=0.0002, beta=0.02):
	print 'starting matrix_factorization'	
	for iteration in xrange(iterations):
		for i in xrange(len(R)):
			for j in xrange(len(R[i])):
				if R[i][j] > 0:
					eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
					for k in xrange(K):
						P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
						Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
		eR = numpy.dot(P,Q)
		e = 0
		for i in xrange(len(R)):
			for j in xrange(len(R[i])):
				if R[i][j] > 0:
					e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
					for k in xrange(K):
						e = e + (beta/2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))
		if e < 0.001:
			break

	print numpy.dot(P, Q)
	return numpy.dot(P, Q)
	
if __name__ == '__main__':
	R = [
			[5,3,0,1],
			[4,0,0,1],
			[1,1,0,5],
			[1,0,0,4],
			[0,1,5,4],
		]

	R = numpy.array(R)
	K = 2

	P = numpy.random.rand(len(R),2)
	Q = numpy.random.rand(2,len(R[0]))

	R_T = matrix_factorization(R, P, Q, K)
