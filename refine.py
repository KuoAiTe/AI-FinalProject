'''
move a point from its current cluster to a nearer one guarrenting the balanced constraints
'''
'''
Refinement: move points between clusters in order to low total distance
    input:
        m_orders: provide features of points
        l_clusters: storage points for each clusters
        m_centroids: provide representatives for clusters
    output:
        l_clusters: new clusters after refining
'''
from general import *
import numpy as np

def findNearCent(point, m_centroids):
    minDist = 99999999
    for i in range(len(m_centroids)):
        if minDist > calDistance(point, m_centroids[i]):
            minDist = calDistance(point, m_centroids[i])
            index = i
    return i

def updateCentroids(m_orders, l_clusters):
    newCentroids = []
    length = len(m_orders[0])
    for i in range(len(l_clusters)):
        tmp = np.array([])
        for j in range(len(l_clusters[i])):
            tmp += np.array(m_orders[l_clusters[i][j]])
        for k in range(length):
            tmp[k] /= len(l_clusters[i])
        newCentroids.append(tmp.tolist())
    return newCentroids

def refining(m_orders, l_clusters, m_centroids, minVolume):
    epsilon = 0.01
    n_clusters = len(l_clusters)
    while True:
        for i in range(n_clusters):
            if len(l_clusters[i]) > minVolume:
                for j in range(len(l_clusters[i])):
                    pointIndex = l_clusters[i][j]
                    bestIndex = findNearCent(m_orders[pointIndex], m_centroids)
                    if i != bestIndex:
                        l_clusters[i].remove(pointIndex)
                        l_clusters[bestIndex].append(pointIndex)
                        j = j - 1
                        if len(l_clusters[i]) <= minVolume:
                            break
        
        newCentroids = updateCentroids(m_orders, l_clusters)
        if np.linalg.norm(m_centroids - newCentroids) <= epsilon:
            break
        else:
            m_centroids = newCentroids

    return l_clusters


            
    