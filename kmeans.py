import numpy as np
import random
from general import *

epsilon = 0.1

class kmeans():
    '''
    input:
        orders: provide features of points
        n_clusters: number of clusters
        d_location: locations of warehouses, (X, Y)
    '''

    def __init__(self, orders, quantityTopic, quantityInvoice, w_location, d_location, c_location, nearWarehouse, n_clusters):
        self.n_cluster = n_clusters
        # self.data = np.loadtxt('A.txt')
        self.n_feature = len(orders[0])
        # self.data = np.random.choice(100, (15000, 10))
        # self.data = orders
        self.nearWarehouse = nearWarehouse
        self.m_order = orders
        self.d_location = d_location
        self.w_location = w_location
        self.c_location = c_location
        self.quantityTopic = quantityTopic
        self.quantityInvoice = quantityInvoice
        self.MaxIteration = 100
        self.dataSize = len(self.m_order)
        self.idx = np.zeros(self.dataSize, dtype = int)
        self.terminal = False


    def initCentroids(self):
        centroids = []
        for i in range(self.n_cluster):
            tmp = np.zeros(self.n_feature).tolist()
            tmp[self.nearWarehouse[i][0]] = 1
            tmp[self.n_feature - 2] = self.d_location[i][0]
            tmp[self.n_feature - 1] = self.d_location[i][1]
            centroids.append(tmp)
        return centroids


    def updateCentroids(self):
        numCluster = np.zeros(self.n_cluster, dtype = int)
        sumCluster = np.zeros((self.n_cluster, self.n_feature))
        for i in range(self.dataSize):
            numCluster[self.idx[i]] += 1
            sumCluster[self.idx[i]] += np.array(self.m_order[i])
        
        for i in range(self.n_cluster):
            for j in range(self.n_feature):
                sumCluster[i][j] /= numCluster[i]
        
        if np.linalg.norm(np.array(self.centroids) - sumCluster) <= epsilon:
            self.terminal = True
        
        self.centroids = sumCluster.tolist()


    def obj(self):
        distortion = 0
        for i in range(self.dataSize):
            distortion += calDistance(self.m_order[i], self.centroids[self.idx[i]]) ** 2
        return distortion


    def assignCluster(self):
        for i in range(self.dataSize):
            min_distance = 99999
            # print('assigning point ' + str(i))
            for k in range(self.n_cluster):
                d = calDistance(self.m_order[i], self.centroids[k])
                if d < min_distance:
                    min_distance = d
                    self.idx[i] = k


    def solve(self):
        self.centroids = self.initCentroids()
        for iteration in range(self.MaxIteration):
            self.assignCluster()
            self.updateCentroids()
            # print('distortion', self.obj(), 'realcost', calObjective(self.quantityTopic, self.quantityInvoice, self.w_location, self.d_location, self.c_location, self.idx))
            print('distortion', self.obj())
            if self.terminal == True:
                break
        

    def getClusters(self):
        clusters = []
        for i in range(self.n_cluster):
            clusters.append([])
        for i in range(self.dataSize):
            clusters[self.idx[i]].append(i)
        return clusters


    def getCentroids(self):
        return self.centroids

    def getIdx(self):
        return self.idx
    
