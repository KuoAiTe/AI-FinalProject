#!/usr/bin/env python
import cPickle
import numpy as np

# pointTopicPortionList
f = open('pointTopicList.pkl','rb')
pointTopicList = cPickle.load(f)
f.close()

pointTopicPortionList = []

for row in pointTopicList:
    tot =  sum(row[:6])
    if tot == 0:
        newRow = row
    else:
        newRow = []
        for i in xrange(6):
            newRow.append(row[i]*1.0/tot)
        newRow = newRow + row[-2:]

    pointTopicPortionList.append(newRow)

print len(pointTopicPortionList)
print pointTopicPortionList[-1]

pointTopicPortionList = np.array(pointTopicPortionList)

f = open('pointTopicPortionList.pkl','wb')
cPickle.dump(pointTopicPortionList,f)
f.close()
