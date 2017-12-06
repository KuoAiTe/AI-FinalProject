"""
Course project of COMP6600
"""
import math
import random
from sample import sample
from preprocess import preprocessor
from sklearn.cluster import KMeans

# dataset preprocessing
fileName = "./data/data.mat"
dataSet = preprocessor(fileName)
m_order = dataSet.get_order()       # m_order is sparse matrix

# Sampling
m_sample_order = sample(m_order)

tmp = []
for i in range(10):
    tmp.append(m_order[:, i])

# Clustering
kmeans = KMeans(n_clusters=20, random_state=0).fit(tmp)
print(kmeans.labels_)

# Populating and Refining


