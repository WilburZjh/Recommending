#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random

class ItemBasedCF:
    def __init__(self, datafile = None):
        self.data = dict()
        for line in open(datafile):
            userid, itemid, rating, utimestamp = line.split()
            self.data.setdefault(userid, dict())
            self.data[userid].setdefault(itemid, 0)
            self.data[userid][itemid] = int(rating)

    def shuffleData(self, k, seed, data = None, M = 8):
        self.traindata = dict()
        self.testdata = dict()
        random.seed(seed)

        for user, item_rating in self.data.items():
            for item, rating in item_rating.items():
                if random.randint(0, M) == k:
                    self.testdata.setdefault(user, dict())
                    self.testdata[user][item] = rating
                else:
                    self.traindata.setdefault(user, dict())
                    self.traindata[user][item] = rating

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
            self.user_average[user] = float(self.user_average[user]/len(train[user].items()))

    def itemSimilarity(self):
        self.itemsimcosine = dict()
        for i, related_items in self.item_item.items():
            self.itemsimcosine.setdefault(i, dict())
            for j, num in related_items.items():
                self.itemsimcosine[i][j] = num / math.sqrt(self.item_user[i] * self.item_user[j])


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

    def recall(self, train = None, test = None, k = 10, N = 10):
        train = train or self.traindata
        test = test or self.testdata
        hit = 0
        recall = 0
        for user in train.keys():
            testuser = test.get(user, dict())
            for item, sim in self.recommend(user, train = train, k = k, N= N).items():
                if item in testuser:
                    hit += 1
            recall += len(testuser)
        return float(float(hit)/float(recall))

    def precision(self, train = None, test = None, k = 10, N = 10):
        print "starting precision"
        train = train or self.traindata
        test = test or self.testdata
        hit = 0
        precision = 0
        for user in train.keys():
            testuser = test.get(user,dict()) 
            for item, sim in self.recommend(user, train = train, k = k, N = N).items():
                if item in testuser:
                    hit += 1
            precision += N
        return float(float(hit)/float(precision))

    def coverage(self, train = None, test = None, k = 10, N = 10):
        print "starting coverage"
        train = train or self.traindata
        test = test or self.testdata
        recommend_items = set()
        all_items = set()
        for user in train.keys():
            for item in train[user].keys():
                all_items.add(item)
            for item, sim in self.recommend(user, train, k = k, N = N).items():
                recommend_items.add(item)
        return float(float(len(recommend_items))/float(len(all_items)))

    def mean_absolute_error(self, train = None, test = None):
        print "starting mae"
        train = train or self.traindata
        test = test or self.testdata
        mae = 0
        count = 0
        bias = 0
        for user, item_rating in train.items():
            tu = test.get(user,dict())
            if len(tu) == 0:
                continue
            for item, rating in tu.items():
                count += 1
                predicted = self.predictRating(user, item)
                bias += abs(rating-predicted)
        mae = float(bias/count)
        return mae

if __name__ == '__main__':
    ibcf = ItemBasedCF('ml-100k/u.data ')
    for k1 in [5, 10, 20, 40, 80, 160]:
        recall = 0
        precision = 0
        coverage = 0
        mae = 0

        for m in [1,2,3,4,5,6,7,8]:
            for seed in [40, 60, 80, 100]:
                ibcf.shuffleData(m, seed)
                ibcf.inverse()
                ibcf.userAverageRating()
                ibcf.itemSimilarity()
                recall += ibcf.recall(k = k1)
                precision += ibcf.precision(k = k1)
                coverage += ibcf.coverage(k = k1)
                mae += ibcf.mean_absolute_error()
        f1 = 2*(recall * precision)/((recall + precision)*32)

        print (k1, float(recall/32) * 100, float(precision/32) * 100, float(coverage/32) * 100,f1)
    mae = float(mae/(6*32))
    print 'The mae is:', mae
