#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math

class UserBasedCF:
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

        return dict(sorted(rank.items(),key = lambda x :x[1],reverse = True)[0:N])
    
    def recall(self, train = None, test = None, k = 10, N = 10):
        print "starting recall"
        train = train or self.traindata
        test = test or self.testdata
        hit = 0
        recall = 0
        for user in train.keys():
            testuser = test.get(user,dict())
            for item, sim in self.recommend(user, train = train, k = k, N = N).items():
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
            for item, sim in self.recommend(user, train = train, k = k, N = N).items():
                recommend_items.add(item)
        return float(float(len(recommend_items))/float(len(all_items)))
              
if __name__ == "__main__":
    ubcf  =  UserBasedCF('/ml-100k/u.data')

    for k1 in [5,10,20,40,80,160]:
        recall = 0
        precision = 0
        coverage = 0
        for m in [1,2,3,4,5,6,7,8]:
            for seed in [40, 60, 80, 100]:
                ubcf.shuffleData(m, seed)
                ubcf.inverse()
                ubcf.userset()
                ubcf.userSimilarity()
                recall += ubcf.recall(k = k1)
                precision += ubcf.precision(k = k1)
                coverage += ubcf.coverage(k = k1)
        f1 = 2*float((recall*precision)/((recall + precision)*32))
        print (k1,float(recall/32 * 100), float(precision/32 * 100),float(coverage/32 * 100), f1)
