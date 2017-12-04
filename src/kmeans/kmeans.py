import numpy as np
import random
class kmeans():
    def __init__(self):
        self.k_cluster= 3
        self.data = np.loadtxt('A.txt')
        self.MaxIteration = 100
        self.dataSize = len(self.data)
        self.idx = np.zeros(self.dataSize,dtype=int)
    def initCentroids(self):
        centroids = []
        idx = random.sample(range(self.dataSize), self.k_cluster)
        for i in range(self.k_cluster):
            centroid = {'x':self.data[idx[i]][0],'y':self.data[idx[i]][1]}
            centroids.append(centroid)
        return centroids

    def updateCentroids(self):
        numCluster = np.zeros(self.k_cluster, dtype=np.int)
        for centroid in self.centroids:
            for key in centroid:
                centroid[key] = 0
        for i in range(self.dataSize):
            clusterID = self.idx[i]
            self.centroids[clusterID]['x'] += self.data[i][0]
            self.centroids[clusterID]['y'] += self.data[i][1]
            numCluster[clusterID] += 1
        for cluster in range(self.k_cluster):
            centroid = self.centroids[cluster]
            for key in centroid:
                if numCluster[cluster] > 0:
                    centroid[key] /= numCluster[cluster]
    def calculateDistance(self,data,centroid):
        c = [centroid['x'], centroid['y']]
        x = np.linalg.norm(data -c )
        return x
    def obj(self):
        distortion = 0
        for i in range(self.dataSize):
                distortion += self.calculateDistance(self.data[i],self.centroids[self.idx[i]]) ** 2
        return distortion
    def assignCluster(self):
        for i in range(self.dataSize):
            min_distance = 99999;
            for k in range(self.k_cluster):
                d = self.calculateDistance(self.data[i],self.centroids[k])
                if d < min_distance:
                    min_distance = d
                    self.idx[i] = k
    def solve(self):
        self.centroids = self.initCentroids()
        for iteration in range(self.MaxIteration):
            self.assignCluster()
            self.updateCentroids()
            print('distortion',self.obj())
a = kmeans()
a.solve()
