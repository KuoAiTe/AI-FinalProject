"""
Author: Ai-Te Kuo
Modified: Chengfei Wang
Last edited: Nov 14, 2017
"""

import sys
import random
import pandas as pd
from dataSet import dataSet

import cPickle
import numpy as np

fileName = "./data/data.mat"
df = dataSet(fileName)
data = df.getData()
m_order = df.getOrder()
print data
print m_order

print len(set(data['StockCode']))

