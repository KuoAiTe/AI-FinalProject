"""
Author: Ai-Te Kuo
Last edited: Dec 3, 2017

"""

import scipy.io as sio
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix

fileName = 'new.csv'
outputFile = 'data.mat'
dataSet = pd.read_csv(fileName, index_col=False)
dataSize = len(dataSet.index)
row = np.zeros(dataSize)
col = np.zeros(dataSize)
data = np.zeros(dataSize)
for index, record in dataSet.iterrows():
    row[index] = 1
    InvoiceNo = record['InvoiceNo']
    StockCode = record['StockCode']
    CustomerID = record['CustomerID']
    Quantity = record['Quantity']
    row[index] = InvoiceNo
    col[index] = StockCode
    data[index] = Quantity
m_order = csr_matrix((data, (row, col)))
a_dict = {col_name : dataSet[col_name].values for col_name in dataSet.columns.values}

sio.savemat(outputFile,{'data':a_dict,'m_order':m_order})
