"""
Course project of COMP6600
"""
import math
import random
import time
from sample import sample
from preprocess import preprocessor
from sklearn.cluster import KMeans
from kmeans import kmeans
from populate import populating
from refine import refining

start = time.clock()

# dataset preprocessing
start_preprocessing = time.clock()
fileName = "./data/data.mat"
dataSet = preprocessor(fileName)
m_order = dataSet.get_order()       # m_order is sparse matrix
topicList = dataSet.get_topicList()
d_location = dataSet.get_dLocation()
w_location = dataSet.get_wLocation()
c_location = dataSet.get_cLocation()
nearWarehouse = dataSet.get_sortedDistanceIndex()
skuKeeping = dataSet.get_skuKeeing()
invoiceList = dataSet.get_quantity()
print('preprocessing takes:', time.clock() - start_preprocessing)

# Sampling
print('Sampleing...')
start_sampling = time.clock()
K = 20      # number of clusters
L = K       # proportion = 1/L
S = 50      # at least S samples are chosen from each partition
P = 0.9    # confidence level
minVolume = 700
m_sample_order, v_sampleID = sample(matrix = m_order, K = K, L = L, S = S, P = P)
print('sampling takes:', time.clock() - start_preprocessing)

# Clustering
print("clustering...")
start_clustering = time.clock()
# km = kmeans(orders = m_sample_order, quantityTopic = topicList, quantityInvoice = invoiceList, w_location = w_location, d_location = d_location, 
#             c_location = c_location, nearWarehouse = nearWarehouse, n_clusters = 20)
# km.solve()
# print(km.idx)
# clusterList = km.getClusters()
# centroidList = km.getCentroids()
# idx = km.getIdx()
print('clustring takes:', time.clock() - start_clustering)



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
#------------------------------------------------------------------------

# Populating
print('Populating...')
start_populating = time.clock()
# clusterList = populating(clusterList)
print('populating takes:', time.clock() - start_populating)

print('Refining...')
start_refining = time.clock()
# clusterList = refining(m_orders = m_order, l_clusters = clusterList, m_centroids = centroidList, minVolume = minVolume)
clusterList = refining(m_orders = m_order, l_clusters = l_clusters, m_centroids = m_centroids, minVolume = minVolume)
print('refining takes:', time.clock() - start_refining)
print('Total time consumption:', time.clock() - start)
