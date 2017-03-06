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

	def itemSimilarity(self, train = None):
		train = train or self.traindata
		item_users = dict()
		for user, item in train.items():
			for i in item.keys():
				item_users.setdefault(i, set())
				item_users[i].add(user)

		item_item = dict()

		for users, related_items in train.items():
			for i in related_items.keys():
				for j in related_items.keys():
					if i==j:
						continue
					item_item.setdefault(i, dict())
					item_item[i].setdefault(j, set())
					item_item[i][j].add(users)

		self.item_item_similarity = dict()
		numerator = 0
		d1 = 0
		d2 = 0

		for i, item_user in item_item.items():
			self.item_item_similarity.setdefault(i, dict())
			for j, users in item_user.items():
				self.item_item_similarity[i].setdefault(j, 0)
				for u in users:
					numerator += (train[u][i]) * (train[u][j])
					d1 += train[u][i] * train[u][i]
					d2 += train[u][j] * train[u][j]
				self.item_item_similarity[i][j] = numerator / math.sqrt(d1 * d2)
				numerator = 0
				d1 = 0
				d2 = 0

			print 'item i:', i, 'item j:', j, 'similarity:', self.item_item_similarity[i][j]

if __name__ == '__main__':
	ibcf = ExampleIbcf('/Users/zhangjinhang1/Documents/University/y4/dissertation/submit/code_4230348/test.data')
	ibcf.itemSimilarity()
