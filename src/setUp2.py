#!/usr/bin/env python

# Chengfei Wang
# this code is randomly set-up 3645 kinds of products
# 
import cPickle
import numpy as np
import matplotlib.pyplot as plt

productStore = []

for i in xrange(3645):
    productStore.append([i,np.random.choice([1,2,3,4,5,6])])

productStore = np.array(productStore)
f = open('productStore.pkl','wb')
cPickle.dump(productStore,f)
f.close()

plt.plot(productStore[:,0],productStore[:,1],'+')
plt.show()
