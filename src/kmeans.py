import pandas as pd
import numpy as np
import random
import time
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
        '''
            DC: Distribution Center [0 ... 0 .... numStorage longitude latitude]
            :param None
            :return centroids <list>
        '''
        centroids = []
        for i in range(self.n_cluster):
            dc = np.zeros(self.n_feature)
            nearWarehouse_index = self.nearWarehouse[i][0]
            longitude_index = self.n_feature -2
            latitude_index = self.n_feature - 1
            longitude = self.d_location[i][0]
            latitude = self.d_location[i][1]
            dc[nearWarehouse_index] = 1
            dc[longitude_index] = longitude
            dc[latitude_index] = latitude
            centroids.append(dc)
        return centroids

    def assignCluster(self):
        '''
            Assign each instance to a cluster
            :param None
            :return distortionValue
        '''
        distortion = np.zeros(self.dataSize)
        for i in range(self.dataSize):
            min_distance = 99999
            for k in range(self.n_cluster):
                d = calDistance(self.m_order[i], self.centroids[k])
                if d < min_distance:
                    min_distance = d
                    distortion[i] = min_distance **2
                    self.idx[i] = k
        distortionValue = sum(distortion)
        return distortionValue

    def updateCentroids(self):
        numCluster = np.zeros(self.n_cluster, dtype = int)
        newCentroids = np.zeros((self.n_cluster, self.n_feature))
        for i in range(self.dataSize):
            numCluster[self.idx[i]] += 1
            newCentroids[self.idx[i]] += self.m_order[i]
        for i in range(self.n_cluster):
                newCentroids[i] /= numCluster[i]
        self.centroids = newCentroids

    def execute(self):
        self.centroids = self.initCentroids()
        previous_distortion = 0
        for iteration in range(self.MaxIteration):
            current_distortion = self.assignCluster()
            distortion_difference = abs(current_distortion - previous_distortion)
            print('distortion',current_distortion)
            print('previous_distortion',previous_distortion)
            print('difference',distortion_difference,'/',current_distortion * epsilon)
            if distortion_difference <= current_distortion * epsilon:
                break
            self.updateCentroids()

            previous_distortion = current_distortion

    def getClusters(self):
        clusters = [[] for _ in range(self.n_cluster)]
        for i in range(self.dataSize):
            clusters[self.idx[i]].append(i)
        return clusters

    def getCentroids(self):
        return self.centroids

    def getIdx(self):
        return self.idx
