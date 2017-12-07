"""
Course project of COMP6600
"""
import math
import random
from sample import sample
from preprocess import preprocessor
from sklearn.cluster import KMeans
from kmeans import kmeans
from populate import populating
from refine import refining


# dataset preprocessing
fileName = "./data/data.mat"
dataSet = preprocessor(fileName)
m_order = dataSet.get_order()       # m_order is sparse matrix

# Sampling
# Parameters:
K = 20      # number of clusters
L = K       # proportion = 1/L
S = 50      # at least S samples are chosen from each partition
P = 0.9    # confidence level
minVolume = 50

m_sample_order = sample(matrix = m_order, K = K, L = L, S = S, P = P)

# tmp = []
# for i in range(10):
#     tmp.append(m_order[:, i])

# Clustering
# kmeans = KMeans(n_clusters=20, random_state=0).fit(tmp)
# print(kmeans.labels_)

km = kmeans(orders = m_order, n_clusters = 20, w_location = w_location)
km.solve()
print(km.idx)
clusterList = km.getClusters()
centroidList = km.getCentroids()

# Populating and Refining
clusterList = populating(clusterList)
clusterList = refining(m_orders = m_order, l_clusters = clusterList, m_centroids = centroidList, minVolume = minVolume)


