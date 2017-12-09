import pandas as pd
import numpy as np
import random
import time
from general import *

epsilon = 1

class kmeans(object):
    '''
    input:
        orders: provide features of points
        n_clusters: number of clusters
        d_location: locations of warehouses, (X, Y)
    '''

    def __init__(self, sample_orders, quantityTopic, quantityInvoice, d_location,  nearWarehouse, n_clusters):
        self.n_cluster = n_clusters
        # self.data = np.loadtxt('A.txt')
        self.n_feature = len(sample_orders[0])
        # self.data = np.random.choice(100, (15000, 10))
        # self.data = orders
        self.nearWarehouse = nearWarehouse
        self.m_sample_orders = sample_orders
        self.d_location = d_location
        self.quantityTopic = quantityTopic
        self.quantityInvoice = quantityInvoice
        self.MaxIteration = 100
        self.sampleSize = len(self.m_sample_orders)
        self.sampleIdx = np.zeros(self.sampleSize, dtype = int)
        self.Verbose = False


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
        distortion = np.zeros(self.sampleSize)
        for i in range(self.sampleSize):
            min_distance = 99999
            for k in range(self.n_cluster):
                d = calDistance(self.m_sample_orders[i], self.centroids[k])
                if d < min_distance:
                    min_distance = d
                    distortion[i] = min_distance **2
                    self.sampleIdx[i] = k
        distortionValue = sum(distortion)
        return distortionValue

    def updateCentroids(self):
        numCluster = np.zeros(self.n_cluster, dtype = int)
        newCentroids = np.zeros((self.n_cluster, self.n_feature))
        for i in range(self.sampleSize):
            numCluster[self.sampleIdx[i]] += 1
            newCentroids[self.sampleIdx[i]] += self.m_sample_orders[i]
        for i in range(self.n_cluster):
                newCentroids[i] /= numCluster[i]
        self.centroids = newCentroids
    '''
    def total_distance(self):
        distortion = 0
        for i in range(self.sampleSize):
            distortion += np.linalg.norm(self.m_sample_orders[i][-2:], self.centroids[self.sampleIdx[i]][-2:])
        return distortion
    '''
    def execute(self):
        self.centroids = self.initCentroids()
        previous_distortion = 0
        for iteration in range(self.MaxIteration):
            current_distortion = self.assignCluster()
            distortion_difference = abs(current_distortion - previous_distortion)
            if self.Verbose:
                print('distortion',current_distortion)
                print('previous_distortion',previous_distortion)
                print('difference',distortion_difference,'/',current_distortion * epsilon)
                #print('obj',self.total_distance())
            if distortion_difference <= current_distortion * epsilon:
                break
            self.updateCentroids()

            previous_distortion = current_distortion

    def getClusters(self):
        clusters = [[] for _ in range(self.n_cluster)]
        for i in range(self.sampleSize):
            clusters[self.sampleIdx[i]].append(i)
        return clusters

    def getCentroids(self):
        return self.centroids

    def getIdx(self):
        return self.sampleIdx
