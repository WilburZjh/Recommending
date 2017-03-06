#!/usr/bin/python
#-*-coding: utf-8 -*-

from mrjob.job import MRJob
from mrjob.step import MRStep
from math import sqrt
from itertools import combinations


class MapReduce(MRJob):

    def user_item_rating(self, key, line):
        uid, iid, rating = line.split('\t')
        yield  uid, (iid, float(rating))

    def counting(self, uid, values):
        iid_rating = list()

        for iid, rating in values:
            iid_rating.append((iid, rating))
        yield uid, (iid_rating)

    def items_rating(self, uid, values):
        for i1, i2 in combinations(values, 2):
            yield (i1[0], i2[0]), (i1[1], i2[1]) 

    def itemitemSim(self, pair_key, lines):
        ii, jj, ij, n = (0, 0, 0, 0)
        item_x, item_y = pair_key       
        for i, j in lines:
            ii += i * i
            jj += j * j
            ij += i * j
            n += 1
        cos_sim = float(ij/(sqrt(ii)*sqrt(jj)))

        yield (item_x, item_y), (cos_sim, n)

    def steps(self):
        return [
            MRStep(mapper=self.user_item_rating,
                   reducer=self.counting),
            MRStep(mapper=self.items_rating,
                   reducer=self.itemitemSim)]
            
if __name__ == '__main__':
    MapReduce.run()