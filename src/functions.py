#!/usr/bin/env python

import cPickle
import numpy as np

f = open('pointList.pkl','rb')
pointList = cPickle.load(f)
f.close()

f = open()

print len(pointList)
print pointList[3]
print pointList[-1]