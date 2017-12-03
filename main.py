"""
Author: Ai-Te Kuo
Last edited: Nov 14, 2017
"""

import sys
import random
import pandas as pd
from dataSet import dataSet

fileName = "./data/data.mat"
df = dataSet(fileName)
data = df.getData()
m_order = df.getOrder()
print(data)
print(m_order)
