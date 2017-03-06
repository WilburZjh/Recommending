#!/usr/bin/python

import math
import random

class WriteFile:
    def __init__(self, datafile = None):
        self.data = dict()
        for line in open(datafile):
            userid, itemid, rating, utimestamp= line.split()
            self.data.setdefault(userid, dict())
            self.data[userid].setdefault(itemid, 0)
            self.data[userid][itemid] = int(rating)

    def shuffleData(self, k, seed, M = 8, data = None):
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

    def writeCsv(self, train = None):
        train = train or self.traindata

        with open('item_user.csv', 'w') as f:
            for user, item_rating in train.items():
                for item, rating in item_rating.items():
                    f.write(item+'|'+user+'|'+str(rating)+'\n')

if __name__ == '__main__':
    wf = WriteFile('/ml-100k/u.data')
    wf.shuffleData(5, 100)
    wf.writeCsv()