import numpy as np
import random
from general import *

class kmeans():
    '''
    input:
        orders: provide features of points
        n_clusters: number of clusters
        w_location: locations of warehouses, (X, Y)
    '''

    def __init__(self, orders, n_clusters, w_location):
        self.n_cluster = n_clusters
        # self.data = np.loadtxt('A.txt')
        self.n_feature = len(orders[0])
        self.data = np.random.choice(100, (15000, 10))
        self.m_order = orders
        self.w_location = w_location
        self.MaxIteration = 100
        self.dataSize = len(self.data)
        self.idx = np.zeros(self.dataSize, dtype = int)
        self.clusters = []

    def initCentroids(self):
        centroids = []
        for i in range(self.n_cluster):
            tmp = np.zeros(self.n_feature).tolist()
            tmp[i] = 1
            tmp[self.n_cluster - 2] = self.w_location[i][0]
            tmp[self.n_cluster - 1] = self.w_location[i][1]
            centroids.append(tmp)
        return centroids

    def updateCentroids(self):
        numCluster = np.zeros(self.n_cluster, dtype = int)
        sumCluster = np.zeros((self.n_cluster, self.n_feature))
        for i in range(self.dataSize):
            numCluster[self.idx[i]] += 1
            sumCluster[self.idx[i]] += np.array(self.data[i])
        
        for i in range(self.n_cluster):
            for j in range(self.n_feature):
                sumCluster[i][j] /= numCluster[i]
        
        self.centroids = sumCluster[i].tolist()

    def obj(self):
        distortion = 0
        for i in range(self.dataSize):
                distortion += calDistance(self.data[i],self.centroids[self.idx[i]]) ** 2
        return distortion

    def assignCluster(self):
        for i in range(self.dataSize):
            min_distance = 99999
            for k in range(self.n_cluster):
                d = calDistance(self.data[i],self.centroids[k])
                if d < min_distance:
                    min_distance = d
                    self.idx[i] = k

    def solve(self):
        self.centroids = self.initCentroids()
        for iteration in range(self.MaxIteration):
            self.assignCluster()
            self.updateCentroids()
            print('distortion',self.obj())
        
    def getClusters(self):
        clusters = []
        for i in range(self.n_cluster):
            clusters.append([])
        for i in range(self.dataSize):
            clusters[self.idx[i]].append(i)
        return clusters

    def getCentroids(self):
        return self.centroids

a = kmeans()
a.solve()