#!/usr/bin/env python

import cPickle
import numpy as np

f = open('pointTopicPortionList.pkl','rb')
pointTopicPortionList = cPickle.load(f)
f.close()

print len(pointTopicPortionList)
print pointTopicPortionList[3]
print pointTopicPortionList[-1]