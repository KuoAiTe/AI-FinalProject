"""
Course project of COMP6600
"""
import math
import random
import pandas as pd
from dataSet import dataSet
from sklearn.cluster import KMeans
from balanced_kmeans import balanced_kmeans

# dataset preprocessing
fileName = "./data/data.mat"
dataSet = dataSet(fileName)
m_order = dataSet.get_order()       # m_order is sparse matrix
topicList = dataSet.get_topicList()

# Sampling
print('Sampleing...')

# Clustering
d_location = dataSet.get_dLocation()
w_location = dataSet.get_wLocation()
c_location = dataSet.get_cLocation()
nearWarehouse = dataSet.get_sortedDistanceIndex()
skuKeeping = dataSet.get_skuKeeping()
invoiceList = dataSet.get_quantity()

print("clustering...")
km =balanced_kmeans(m_order = m_order, quantityTopic = topicList, quantityInvoice = invoiceList, d_location = d_location, nearWarehouse = nearWarehouse, n_clusters = 20)
km.execute()


#print(km.idx)

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

# with open('centroid.txt', 'w') as f:
#     for i in range(len(centroidList)):
#         f.write(str(centroidList[i]) + '\n')
#     f.close()
# with open('idx.txt', 'w') as f:
#     for i in range(len(idx)):
#         f.write(str(idx[i]) + '\n')
#     f.close()
# with open('sampleID.txt', 'w') as f:
#     for i in range(len(v_sampleID)):
#         f.write(str(v_sampleID[i]) + '\n')
#     f.close()
# with open('sampleID.txt', 'w') as f:
#     for i in range(len(v_sampleID)):
#         f.write(str(v_sampleID[i]) + '\n')
#     f.close()


#------------------------------------------------------------------------
'''
f = open('centroid.txt')
m_centroids = []
for each in f:
    m_centroids.append(int(each))
f.close()
f = open('idx.txt')
idx = []
for each in f:
    idx.append(int(each))
f.close()
l_clusters = []
for j in range(len(m_centroids)):
    l_clusters.append([])
for i in range(len(m_order)):
    l_clusters[idx[i]].append(i)
'''
#------------------------------------------------------------------------

# Populating and Refining
# clusterList = populating(clusterList)
# clusterList = refining(m_orders = m_order, l_clusters = clusterList, m_centroids = centroidList, minVolume = minVolume)
'''print('Refining...')
clusterList = refining(m_orders = m_order, l_clusters = l_clusters, m_centroids = m_centroids, minVolume = minVolume)
'''
