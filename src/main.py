"""
Author: Ai-Te Kuo
Last edited: Nov 14, 2017
"""

import sys
import random
import pandas as pd
from dataSet import dataSet

from sklearn.cluster import KMeans


fileName = "./data/data.mat"
df = dataSet(fileName)
#data = df.getData()
#m_order = df.getOrder()
