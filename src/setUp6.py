#!/usr/bin/env python

import cPickle
import numpy as np

f = open('pointList.pkl','rb')
pointList = cPickle.load(f)
f.close()

f = open('productStore.pkl','rb')
productStore = cPickle.load(f)
f.close()

f = open('customerLocation.pkl','rb')
customerLocation = cPickle.load(f)
f.close()

pointTopicList = []
'''
print pointList[0], customerLocation[pointList[0]['CustomerID']]

for key in pointList[0]:
    if key != 'CustomerID':
        print key
        print productStore[key][1] - 1

'''
progress = 0

for each in pointList:
    #print each
    location = [0,0]
    location[0] = customerLocation[each['CustomerID']][0]
    location[1] = customerLocation[each['CustomerID']][1]
    # there are only 6 stores
    count = [0,0,0,0,0,0]
    for key in each:
        if key != 'CustomerID':
            s = productStore[key][1] - 1
            count[s-1] += each[key]
    newRow = count + location
    pointTopicList.append(newRow)

print pointTopicList[-1]
print len(pointTopicList)

f = open('pointTopicList.pkl','wb')
cPickle.dump(pointTopicList,f)
f.close()
    




