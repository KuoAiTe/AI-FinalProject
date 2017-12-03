"""
Author: Ai-Te Kuo
Last edited: Nov 14, 2017

http://archive.ics.uci.edu/ml/datasets/online+retail
Data Set Information:

This is a transnational data set which contains all the transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail.
The company mainly sells unique all-occasion gifts. Many customers of the company are wholesalers.

Attribute Information:

InvoiceNo: Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation.
StockCode: Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.
Quantity: The quantities of each product (item) per transaction. Numeric.
CustomerID: Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer.

['InvoiceNo' 'StockCode' 'CustomerID' 'Quantity']
"""
import pandas as pd
import numpy as np
import scipy.io as sio
from scipy.sparse import csr_matrix
import os
class dataSet():
    def __init__(self, fileName=None):
        self.__dataSet = None
        if fileName is not None:
            self.loadDataSet(fileName)
    def loadDataSet(self, fileName = None):
        if(fileName is None):
            raise ValueError("DataSet.loadDataSet: No file is provided.")
        if(type(fileName) is not str):
            raise ValueError("DataSet.loadDataSet: fileName must be a string.")
        if(len(fileName) < 4):
            raise ValueError("DataSet.loadDataSet: Input file name is too short.")
        if(not os.path.isfile(fileName)):
            raise ValueError("DataSet.loadDataSet: File is not found.")
        self.__dataSet = sio.loadmat(fileName)
        d = self.__dataSet['data']
        InvoiceNo = d['InvoiceNo'][0][0][0]
        StockCode = d['StockCode'][0][0][0]
        CustomerID =d['CustomerID'][0][0][0]
        Quantity = d['Quantity'][0][0][0]
        self.__data = pd.DataFrame({'InvoiceNo':InvoiceNo,'StockCode':StockCode,'CustomerID':CustomerID,'Quantity':Quantity})
    def getData(self):
        return self.__data
    def getOrder(self):
        return self.__dataSet['m_order']
