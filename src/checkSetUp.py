#!/usr/bin/env python
import cPickle
import numpy as np
import matplotlib.pyplot as plt

f = open('customerLocation.pkl','rb')
customerLocation = cPickle.load(f)
f.close()

print max(customerLocation[:,0]),min(customerLocation[:,0])
print max(customerLocation[:,1]),min(customerLocation[:,1])
plt.plot(customerLocation[:,0],customerLocation[:,1],'+')
plt.show()

f = open('productStore.pkl','rb')
productStore = cPickle.load(f)
f.close()

plt.plot(productStore[:,0],productStore[:,1],'+')
plt.show()
