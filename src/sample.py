import math
import random
import numpy as np
def sample(matrix, K, L, S, P):
    '''
        C = math.log(1/(1 - P), K) chosen constant

        :param K = 20  number of clusters
        :param L = K   proportion = 1/L
        :param S = 50  at least S samples are chosen from each partition
        :param P = 0.9 confidence level
        :return sampleSet
        :return sampleSetIdx
    '''
    C = math.log(1/(1 - P), K)
    num_sample = int(math.ceil(C*S*L*math.log(K)))
    num_order = len(matrix)
    sampleSet = []
    sampleSetIdx = random.sample(np.arange(num_order), num_sample)
    for i in range(0, num_sample):
        sample = matrix[sampleSetIdx[i]]
        sampleSet.append(sample)
    return sampleSet, sampleSetIdx
