#!/usr/bin/env python

# need difination of distance() and represent()
#
def populating(clusterList, balanceFraction):
    for i in xrange(len(clusterList)):
        shortfall[i] = max(balanceFraction - len(clusterList[i]),0)

    d = distance(pointList[0],represent(clusterList[0])) + 1

    for p in pointList:
        for i in xrange(len(clusterList)):
            newD = distance(p, represent(clusterList[i]))
            if newD < d and shortfall[i] > 0:
                shortfall[i] = shortfall[i] - 1
                d = newD
                clusterList[i].append(p)

    return clusterList