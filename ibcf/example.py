#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random

class ExampleIbcf:
	def __init__(self, datafile = None):
		self.traindata = dict()
		for line in open(datafile):
			userid, itemid, rating = line.split()
			self.traindata.setdefault(userid, dict())
			self.traindata[userid].setdefault(itemid, 0)
			self.traindata[userid][itemid] = int(rating)

	def inverse(self, train = None):
		train = train or self.traindata
		self.item_item = dict()
		self.item_user = dict()

		for user, items in train.items():
			for i in items.keys():
				self.item_user.setdefault(i, 0)
				self.item_user[i] += 1
				for j in items.keys():
					if i == j:
						continue
					self.item_item.setdefault(i, dict())
					self.item_item[i].setdefault(j, 0)
					self.item_item[i][j] += 1

	def userAverageRating(self, train = None):
		train = train or self.traindata
		self.user_average = dict()
		for user, item_rating in train.items():
			self.user_average.setdefault(user, 0)
			for item, rating in item_rating.items():
				self.user_average[user] += rating
			self.user_average[user] = (self.user_average[user]/len(train[user].items()))
			print 'user:', user, 'average-rating:', self.user_average[user]

	def itemSimilarity(self):
		self.itemsimcosine = dict()
		for i, related_items in self.item_item.items():
			self.itemsimcosine.setdefault(i, dict())
			for j, num in related_items.items():
				self.itemsimcosine[i][j] = num / math.sqrt(self.item_user[i] * self.item_user[j])
				print 'item i:', i, 'item j:', j, 'similarity:', self.itemsimcosine[i][j]


	def predictRating(self, user, item, train = None):
		train = train or self.traindata
		numerator = 0
		count = 0
		rank = dict()

		if item not in self.itemsimcosine.keys():
			return self.user_average[user]

		for i, sim in sorted(self.itemsimcosine[item].items(), key = lambda x : x[1], reverse = True):
			rank.setdefault(i, 0)
			if i in train[user].keys():
				numerator += sim * train[user][i]
			else:
				numerator += self.user_average[user]
			count += 1
		rank[item] = float(numerator/count)

		print 'user:', user, 'item:', item, 'rating:', rank[item]
		return rank[item]

	def recommend(self, user, train = None, k = 10, N = 30): # N represents the items that want to recommend to users, K represents the sim users that sim to user 
		train = train or self.traindata                     
		rank = dict()
		rec = dict()
		interacted_items = train.get(user,dict())

		for item, rating in train[user].items():
			for i, sim in sorted(self.itemsimcosine[item].items(), key = lambda x : x[1], reverse = True)[0:k]:
				if i not in rank.keys():
					rank.setdefault(i,0)
				if i in interacted_items.keys():
					continue                                                
				rank[i] += self.predictRating(user, i)
		return dict(sorted(rank.items(), key = lambda x : x[1], reverse = True)[0:N])

if __name__ == '__main__':
	ibcf = ExampleIbcf('test.data')
	ibcf.inverse()
	ibcf.userAverageRating()
	ibcf.itemSimilarity()
	ibcf.predictRating('5','5')
