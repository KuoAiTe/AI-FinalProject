import numpy as np
import random
import time

class kmeans():
    def __init__(self):
        self.k_cluster= 20
        self.data = np.loadtxt('B.txt')
        self.data = np.random.choice(2, (15000, 20))
        self.MaxIteration = 100
        self.dataSize = len(self.data)
        self.featureSize = len(self.data[0])
        self.idx = np.zeros(self.dataSize,dtype=int)
        self.a = 0

    def initCentroids(self):
        centroids = []
        # idx = random.sample(range(self.dataSize), self.k_cluster)
        for i in range(self.k_cluster):
            centroid = np.random.randint(0, 2, self.featureSize)
            centroids.append(centroid)
        return centroids

    def updateCentroids(self):
        # numCluster = np.zeros(self.k_cluster, dtype=np.int)
        # for centroid in self.centroids:
        #     for key in centroid:
        #         centroid[key] = 0
        # for i in range(self.dataSize):
        #     clusterID = self.idx[i]
        #     self.centroids[clusterID]['x'] += self.data[i][0]
        #     self.centroids[clusterID]['y'] += self.data[i][1]
        #     numCluster[clusterID] += 1
        # for cluster in range(self.k_cluster):
        #     centroid = self.centroids[cluster]
        #     for key in centroid:
        #         if numCluster[cluster] > 0:
        #             centroid[key] /= numCluster[cluster]

        newCentroids = np.zeros((self.k_cluster, self.featureSize), dtype = np.int)
        clusterVolume = np.zeros(self.k_cluster)
        for i in range(self.dataSize):
            clusterVolume[self.idx[i]] = clusterVolume[self.idx[i]] + 1
            for j in range(self.featureSize):
                newCentroids[self.idx[i]][j] = newCentroids[self.idx[i]][j] + self.data[i][j]
        
        for i in range(self.k_cluster):
            for j in range(self.featureSize):
                if newCentroids[i][j] >= clusterVolume[i]/2:
                    newCentroids[i][j] = 1
                else:
                    newCentroids[i][j] = 0
        self.centroids = newCentroids

    def calculateDistance(self,data,centroid):
        # c = [centroid['x'], centroid['y']]
        # x = np.linalg.norm(data - c)
        x = 0
        for i in range(self.featureSize):
            if data[i] != centroid[i]:
                x = x + 1
        return x

    def obj(self):
        distortion = 0
        for i in range(self.dataSize):
            distortion += self.calculateDistance(self.data[i],self.centroids[self.idx[i]])
        return distortion

    def assignCluster(self):
        for i in range(self.dataSize):
            min_distance = 99999
            for k in range(self.k_cluster):
                d = self.calculateDistance(self.data[i],self.centroids[k])
                if d < min_distance:
                    min_distance = d
                    self.idx[i] = k

    def solve(self):
        self.centroids = self.initCentroids()
        for iteration in range(self.MaxIteration):
            self.assignCluster()
            print(self.idx)
            self.updateCentroids()
            print('distortion',self.obj())


start = time.clock()
# random categorical data
# data = np.random.choice(2, (15000, 3000))
# data = np.loadtxt('B.txt')
k_cluster= 20
a = kmeans()
a.solve()
print(a.idx)

elapsed = (time.clock() - start)
print("Time used:",elapsed)