#!/usr/bin/env python

# Chengfei Wang
# this code is randomly set-up 2d location of 20 distribution centers
# range from 0~1 
#
import cPickle
import numpy as np
import matplotlib.pyplot as plt

centerLocation = np.random.normal(loc = 0.5,scale = 0.13, size = (20,2))
print max(centerLocation[:,0]),min(centerLocation[:,0])
print max(centerLocation[:,1]),min(centerLocation[:,1])
f = open('centerLocation.pkl','wb')
cPickle.dump(centerLocation,f)
f.close()

plt.plot(centerLocation[:,0],centerLocation[:,1],'+')
plt.show()
