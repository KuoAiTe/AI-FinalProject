#!/usr/bin/env python

# Chengfei Wang
# this code is randomly set-up 2000 kinds of products
# 
import cPickle
import numpy as np
import matplotlib.pyplot as plt

productStore = []

for i in xrange(2000):
    productStore.append([i,np.random.choice([1,2,3,4,5,6,7,8,9,10])])

productStore = np.array(productStore)
f = open('productStore.pkl','wb')
cPickle.dump(productStore,f)
f.close()

plt.plot(productStore[:,0],productStore[:,1],'+')
plt.show()
