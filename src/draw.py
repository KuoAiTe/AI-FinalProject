#!/usr/bin/env python

# drawing the set up
import cPickle
import numpy as np
import matplotlib.pyplot as plt

f = open('customerLocation.pkl','rb')
customerLocation = cPickle.load(f)
f.close()

f = open('centerLocation.pkl','rb')
centerLocation = cPickle.load(f)
f.close()

f = open('storeLocation.pkl','rb')
storeLocation = cPickle.load(f)
f.close()

print customerLocation[-1]
print centerLocation[-1]
print storeLocation[-1]
plt.plot(customerLocation[:,0],customerLocation[:,1],'+')
plt.plot(storeLocation[:,0],storeLocation[:,1],'^')
plt.plot(centerLocation[:,0],centerLocation[:,1],'rx')

plt.show()