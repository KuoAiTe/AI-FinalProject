from kmeans import kmeans
from sample import sample
from general import Calculator
import time
import numpy as np
class balanced_kmeans(kmeans):
    def __init__(self, m_order, quantityTopic, quantityInvoice, w_location, d_location, c_location, nearWarehouse, n_clusters,minVolume):
        self.m_order = m_order
        self.dataSize = len(self.m_order)
        self.idx = np.zeros(self.dataSize, dtype = int)
        self.w_location = w_location
        self.c_location = c_location
        self.minVolume = minVolume
        K = 20      # number of clusters
        L = K       # proportion = 1/L
        S = 50      # at least S samples are chosen from each partition
        P = 0.9    # confidence level
        m_sample_order, m_sample_order_idx = sample(matrix = m_order, K = K, L = L, S = S, P = P)
        self.m_sample_order_idx = m_sample_order_idx
        super(balanced_kmeans,self).__init__(m_sample_order, quantityTopic, quantityInvoice, d_location, nearWarehouse, n_clusters)
    def getClusters(self):
        clusters = [[] for _ in range(self.n_cluster)]
        for i in range(self.dataSize):
            clusters[self.idx[i]].append(i)
        return clusters

    def getObj(self):
        distortion = 0
        for i in range(self.sampleSize):
            distortion += Calculator.calDistance(self.m_sample_orders[i], self.centroids[self.sampleIdx[i]])
        return distortion

    def getIdx(self):
        return self.idx

    def populate(self):
        n_clusters = self.n_cluster
        # mapping the sample cluster result to idx
        for i in range(len(self.sampleIdx)):
            idx = self.m_sample_order_idx[i]
            self.idx[idx] = self.sampleIdx[i]

        # create an unsampleSet that removes all samples used in kmeans
        unSampleIdx = set(range(self.dataSize))
        for sampleIdx in self.m_sample_order_idx:
            unSampleIdx.remove(sampleIdx)

        # Check how many available spots in a cluster
        availableSpot = [ 0 for _ in range(n_clusters)]
        clusterList = super(balanced_kmeans,self).getClusters()

        for i in range(n_clusters):
            availableSpot[i] = max(self.minVolume - len(clusterList[i]),0)

        centroids = super(balanced_kmeans,self).getCentroids()
        for sampleIdx in unSampleIdx:
            instance = self.m_order[sampleIdx]
            minDistance = 1000000
            clusterIdx = -1
            for i in range(n_clusters):
                if availableSpot[i] > 0:
                    centroid = centroids[i]
                    if Calculator.calDistance(instance,centroid) < minDistance:
                        minDistance = Calculator.calDistance(instance,centroid)
                        clusterIdx = i

            if clusterIdx > -1:
                availableSpot[clusterIdx] -= 1
                self.idx[sampleIdx] = clusterIdx
            else:
                for i in range(n_clusters):
                    centroid = centroids[i]
                    if Calculator.calDistance(instance,centroid) < minDistance:
                        minDistance = Calculator.calDistance(instance,centroid)
                        clusterIdx = i
                if clusterIdx > -1:
                    availableSpot[clusterIdx] -= 1
                    self.idx[sampleIdx] = clusterIdx
                else:
                    print("Warning")
    def findNearestCentroid(self,instance, centroids):
        minDist = 99999999
        for i in range(len(centroids)):
            distance = Calculator.calDistance(instance, centroids[i])
            if minDist > distance:
                minDist = distance
                index = i
        return index
    def updateCentroids_Refine(self,m_orders, clusterList):
        newCentroids = []
        n_features = len(m_orders[0])
        for i in range(len(clusterList)):
            tmp = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            n_points = len(clusterList[i])
            for j in range(n_points):
                # tmp += np.array(m_orders[clusterList[i][j]])
                tmp += m_orders[clusterList[i][j]]
            for k in range(n_features):
                tmp[k] /= n_points
            newCentroids.append(tmp.tolist())
        return np.array(newCentroids)

    def total_obj(self):
        distortion = 0
        for i in range(self.dataSize):
            distortion += Calculator.calDistance(self.m_order[i], self.centroids[self.idx[i]])
        return distortion

    def refine(self):
        '''
        move a point from its current cluster to a nearer one guarrenting the balanced constraints
        '''
        '''
        Refinement: move points between clusters in order to low total distance
            input:
                m_orders: provide features of points
                clusterList: storage points for each clusters
                m_centroids: provide representatives for clusters
            output:
                clusterList: new clusters after refining
        '''
        epsilon = 0.1
        n_clusters = self.n_cluster
        m_orders = self.m_order
        minVolume = self.minVolume
        centroids = super(balanced_kmeans,self).getCentroids()
        clusterList = self.getClusters()

        while True:
            numCluster = [len(clusterList[i]) for i in range(n_clusters)]
            #print(numCluster)

            for clusterIdx in range(n_clusters):
                if numCluster[clusterIdx] > minVolume:
                    for j in range(numCluster[clusterIdx]):
                        if j >= len(clusterList[clusterIdx]): break
                        instanceIdx = clusterList[clusterIdx][j]
                        bestIndex = self.findNearestCentroid(m_orders[instanceIdx], centroids)
                        if clusterIdx != bestIndex:
                            self.idx[instanceIdx] = bestIndex
                            #print('idx',instanceIdx,'original',clusterIdx,'after',bestIndex)
                            numCluster[bestIndex] +=1
                            numCluster[clusterIdx] -=1
                            if numCluster[clusterIdx] <= minVolume:
                                break

            clusterList = self.getClusters()
            numCluster = [len(clusterList[i]) for i in range(n_clusters)]
            #print(numCluster)
            newCentroids = self.updateCentroids_Refine(m_orders, clusterList)
            print('Objective value after refining:', Calculator.calObjective(self.quantityTopic, self.quantityInvoice, self.w_location, self.d_location, self.c_location, self.idx))
            #print('obj',self.total_obj())
            if np.linalg.norm(centroids - newCentroids) <= epsilon:
                break
            centroids = newCentroids
        self.centroids = centroids

    def execute(self):
        super(balanced_kmeans,self).execute()
        g = time.time()
        self.populate()
        self.refine()
        objValue = Calculator.calObjective(self.quantityTopic, self.quantityInvoice, self.w_location, self.d_location, self.c_location, self.idx)
        return objValue
