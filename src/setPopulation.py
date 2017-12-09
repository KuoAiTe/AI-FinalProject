#!/usr/bin/env python

# input: 
#   idx.txt (how each one of 2k samples belong to each cluster)
#   sampleID.txt (which points are sampled)
#   centroid.txt (how the inital centroids for each)
# output: 
#   save the result in clusterList.pkl

import re
import cPickle
import numpy as np

def distance(point1, point2, alpha=0.5, beta=0.5):
    d1 = sum((point1[:-2] - point2[:-2])**2)**0.5
    d2 = sum((point1[-2:] - point2[-2:])**2)**0.5
    return d1*alpha + d2*beta

# the balancing fraction is 700 for b almost 0.8
N = 16649
m = 700
k = 20

# get un-sampled points
sampleIDList = []
remainingPointsIndex = set(range(16649))
f = open('sampleID.txt')
for each in f:
    sampleIDList.append(int(each))
    if int(each) in remainingPointsIndex:
        remainingPointsIndex.remove(int(each))
f.close()
# print(len(remainingPointsIndex))
# 14346

clusterList = [set() for _ in xrange(k)]
iRow = 0
f = open('idx.txt')
for each in f:
    clusterList[int(each)].add(sampleIDList[iRow])
    iRow += 1
f.close()
# tot = 0
# for each in clusterList:
#     print len(each)
#     tot += len(each)
# print tot
# 2303

centroidList =[]
f = open('centroid.txt')
for eachRow in f:
    centroidList.append(map(float,re.findall(r'[+-]?[0-9.]+', eachRow)))
f.close()
# print len(centroidList[-1])
# 8

f = open('pointTopicPortionList.pkl')
pointTopicPortionList = cPickle.load(f)
f.close()
# print len(pointTopicPortionList)
# 16649

def distance(p1, p2, alpha=0.5, beta=0.5):

    d1 = sum((p1[:-2] - p2[:-2])**2)**0.5
    d2 = sum((p1[-2:] - p2[-2:])**2)**0.5
    return d1*alpha + d2*beta

minVolume = [ 0 for _ in xrange(len(clusterList))]
for i in xrange(len(clusterList)):
    minVolume[i] = max(m - len(clusterList[i]),0)

for j in remainingPointsIndex:
    p = pointTopicPortionList[j]
    belongIndex = 0
    p1 = np.array(p)
    p2 = np.array(centroidList[0])
    minDistance = distance(p1,p2)
    for i in xrange(1,len(clusterList)):
        p2 = np.array(centroidList[i])
        if distance(p1,p2) < minDistance and minVolume[i] > 0 :
            minDistance = distance(p1,p2)
            belongIndex = i
    minVolume[belongIndex] -= 1
    clusterList[belongIndex].add(j)
# tot = 0
# for each in clusterList:
#     print len(each)
#     tot += len(each)
# print tot

f = open('clusterList.pkl','wb')
cPickle.dump(clusterList,f)
f.close()





