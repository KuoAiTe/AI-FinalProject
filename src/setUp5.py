#!/usr/bin/env python

# Chengfei Wang
# this code is randomly set-up 2d location of 6 store
# range from 0~1, and the label of stores are 1~6, so becareful
 
import cPickle
import numpy as np
import matplotlib.pyplot as plt

storeLocation = np.array([[0.912,0.471],[0.765,0.824],[0.295,0.835],
    [0.165,0.524],[0.341,0.241],[0.753,0.247]])

print max(storeLocation[:,0]),min(storeLocation[:,0])
print max(storeLocation[:,1]),min(storeLocation[:,1])
f = open('storeLocation.pkl','wb')
cPickle.dump(storeLocation,f)
f.close()

plt.plot(storeLocation[:,0],storeLocation[:,1],'+')
plt.show()
