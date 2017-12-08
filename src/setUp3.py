#!/usr/bin/env python

"""
Author: Ai-Te Kuo
Modified: Chengfei Wang
Last edited: Nov 14, 2017
"""

# store the 16649 points
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
#print m_order
print data[5:10]
cc = data['Quantity']

pointList = [{} for _ in xrange(16649)]

count = 0
for index, row in data.iterrows():
    count += 1
    if count >= 10000:
        print index
        count = 0

    CustomerID, InvoiceNo, Quantity, StockCode = row

    if StockCode not in pointList[InvoiceNo]:
        pointList[InvoiceNo][StockCode] = Quantity
    else:
        pointList[InvoiceNo][StockCode] += Quantity

    if 'CustomerID' not in pointList[InvoiceNo]:
        pointList[InvoiceNo]['CustomerID'] = CustomerID


f = open('pointList.pkl','wb')
cPickle.dump(pointList,f)
f.close()

