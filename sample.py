import math
import random
import numpy as np

def sample(matrix, K, L, S, P):
    # K = 20      # number of clusters
    # L = K       # proportion = 1/L
    # S = 50      # at least S samples are chosen from each partition
    # # C = 1       # chosen constant
    # P = 0.9    # confidence level
    C = math.log(1/(1 - P), K)
    num_sample = int(math.ceil(C*S*L*math.log(K)))
    # num_sample = 1

    
    num_order = np.array(matrix).shape[0]
    # num_order = 100
    # m_sample_order = matrix.sample(n = 100)
    v_sampleID = random.sample(range(0, num_order), num_sample)

    m_sample = []
    for i in range(0, len(v_sampleID)):
        # m_sample_order.append(np.ndarray.tolist(m_order[i].toarray())[0])
        m_sample.append(matrix[v_sampleID[i]])
    
    return m_sample, v_sampleID