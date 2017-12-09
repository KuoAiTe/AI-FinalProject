# -*- coding: utf-8 -*-
import math
import random
import pandas as pd
import matplotlib.pyplot as plt
import sys
from general import Calculator
from dataSet import dataSet
from sklearn.cluster import KMeans
from balanced_kmeans import balanced_kmeans
reload(sys)
sys.setdefaultencoding('utf8')

fileName = "./data/data.mat"
dataSet = dataSet(fileName)
m_order = dataSet.get_order()
topicList = dataSet.get_topicList()
d_location = dataSet.get_dLocation()
w_location = dataSet.get_wLocation()
c_location = dataSet.get_cLocation()
nearWarehouse = dataSet.get_sortedDistanceIndex()
skuKeeping = dataSet.get_skuKeeping()
invoiceList = dataSet.get_quantity()

_alpha = [i*0.01 for i in range(101)]

for minVolume in [500,600,700,800]:
    _obj = []
    for alpha in _alpha:
        Calculator.setAlpha(alpha)
        km = balanced_kmeans(m_order = m_order, quantityTopic = topicList, quantityInvoice = invoiceList, w_location = w_location, d_location = d_location, c_location = c_location, nearWarehouse = nearWarehouse, n_clusters = 20,minVolume = minVolume)
        objValue = km.execute()
        _obj.append(objValue)
        print('m =%d | α: %f Cost:%f' % (minVolume,alpha,objValue))
    plt.plot(_alpha,_obj, label='m = %d' % minVolume)
plt.xlim((0, 1))
plt.xlabel('α')
plt.ylabel('Cost')
plt.legend()
plt.show()

'''
clusterList = km.getClusters()
centroidList = km.getCentroids()
idx = km.getIdx()

columns=['Storage %d' % i for i in range(len(m_order[0]) - 2)]
columns+= ['Longitude','Latitude']
df = pd.DataFrame(data=centroidList,columns=columns)
df.index.name = 'DC#'
df.to_csv('./result/centroids.csv')
# Save Centroids
df = pd.DataFrame(data=clusterList)
df.index.name = 'Cluster#'
df.to_csv('./result/cluster.csv')
df = pd.DataFrame(data=idx)
df.index.name = 'idx#'
df.to_csv('./result/idx.csv')
'''
