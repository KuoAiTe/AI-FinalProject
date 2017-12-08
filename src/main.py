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
CustomerLocation = df.getCustomerLocation()
ProductStorage = df.getProductStorage()
InvoiceList = df.getInvoiceList()
StorageLocation = df.getStorageLocation()
DC = df.getDC()
TopicList = df.getTopicList()
Distance = df.getDistance()
SortedDistanceIndex = df.SortedDistanceIndex
NormalizedTopicList = df.getNormalizedTopicList()
#print('CustomerLocation',CustomerLocation)
#print('ProductStorage',ProductStorage)
#print(InvoiceList)
#print('StorageLocation',StorageLocation)
#print('Distribution Centers',DC)
#print('TopicList',TopicList)
