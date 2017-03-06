#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random

class ExampleUbcf:
	def __init__(self, datafile = None):
		self.traindata = dict()
		for line in open(datafile):
			userid, itemid, rating = line.split()
			self.traindata.setdefault(userid, dict())
			self.traindata[userid].setdefault(itemid, 0)
			self.traindata[userid][itemid] = int(rating)

	def inverse(self, train = None):
		train = train or self.traindata
		self.item_users = dict()
		for u, item_rating in train.items():
			for i in item_rating.keys():
				self.item_users.setdefault(i,set())
				self.item_users[i].add(u)

	def userset(self):
		self.user_item = dict()
		self.itemcount = dict()
		for item, users in self.item_users.items():
			for u in users:
				self.user_item.setdefault(u, 0)
				self.user_item[u] += 1
				for v in users:
					if u == v:
						continue
					self.itemcount.setdefault(u,dict())
					self.itemcount[u].setdefault(v, 0)
					self.itemcount[u][v] += 1

	def userSimilarity(self):
		self.usersmilarity = dict()
		for u, user_sim in self.itemcount.items():
			self.usersmilarity.setdefault(u,dict())
			for v, sim in user_sim.items():
				self.usersmilarity[u][v] = sim / math.sqrt(self.user_item[u] * self.user_item[v] * 1.0)
				print 'user u:', u, 'user v:', v, 'similarity:', self.usersmilarity[u][v]

	def recommend(self, user, k = 10, N = 10, train = None):
		train = train or self.traindata
		rank = dict()
		interacted_items = train.get(user,dict())

		for u, sim in sorted(self.usersmilarity[user].items(),key = lambda x : x[1],reverse = True)[0:k]:
			for i, rating in train[u].items():
				if i in interacted_items:
					continue               
				rank.setdefault(i, 0)
				rank[i] += sim * rating

			print 'user:', u, 'item:', i, 'interest:', rank[i]
		return dict(sorted(rank.items(),key = lambda x :x[1],reverse = True)[0:N])

if __name__ == '__main__':
	ubcf = ExampleUbcf('test.data')
	ubcf.inverse()
	ubcf.userset()
	ubcf.userSimilarity()
	ubcf.recommend('5')
