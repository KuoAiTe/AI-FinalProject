#!/usr/bin/env python

# Chengfei Wang
# this code is randomly set-up 2d location of 3644 customers
# 
import cPickle
import numpy as np
import matplotlib.pyplot as plt

customerLocation = np.random.normal(loc = 0.5,scale = 0.13, size = (3644,2))
print max(customerLocation[:,0]),min(customerLocation[:,0])
print max(customerLocation[:,1]),min(customerLocation[:,1])
f = open('customerLocation.pkl','wb')
cPickle.dump(customerLocation,f)
f.close()

plt.plot(customerLocation[:,0],customerLocation[:,1],'+')
plt.show()
