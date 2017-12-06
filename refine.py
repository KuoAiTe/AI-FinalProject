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
    return i, minDist

def updateCentroids(m_orders, l_clusters):
    newCentroids = []
    length = len(m_orders[0])
    for i in range(len(l_clusters)):
        tmp = []
        for j in range(len(l_clusters[i])):
            tmp = tmp + m_orders[l_clusters[i][j]]
        for  j in range(length):
            tmp[j] = tmp[j] / length
        newCentroids.append(tmp)
    return newCentroids

def refining(m_orders, l_clusters, m_centroids, minVolume):
    epsilon = 0.001
    while True:
        for i in range(len(l_clusters)):
            if len(l_clusters[i]) >= minVolume + 1:
                for j in range(len(l_clusters[i])):
                    pointIndex = l_clusters[i][j]
                    bestIndex, bestDist = findNearCent(m_orders[pointIndex], m_centroids)
                    if i != bestIndex:
                        l_clusters[i].remove(pointIndex)
                        l_clusters[bestIndex].append(pointIndex)
        
        newCentroids = updateCentroids(m_orders, l_clusters)
        if np.linalg.norm(m_centroids - newCentroids) <= epsilon:
            break

    return l_clusters


            
    