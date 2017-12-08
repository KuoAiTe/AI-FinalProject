#
# Author: Ai-Te Kuo, Chengfei Wang
# Last Modified: Dec 7, 2017
#
import os
import numpy as np
import cPickle
import scipy.io as sio
import pandas as pd
import matplotlib.pyplot as plt
class dataSet():
    def __init__(self,fileName = "./data/data.mat", numStorage = 6, numDC = 20,Verbose = True):
        '''
        Parameters:
        self.customerSize: The number of customers
        self.numItem: The number of unique stockCode
        self.numStorage: The number of storage
        self.numInvoice: The number of unique invoiceNo
        self.numDC: The number of distribution centers
        self.Longitude_Base: The longitude of the center of customers, based on Oxford
        self.Latitude_Base: The latitude of the center of customers, based on Oxford
        '''
        self.Verbose = Verbose
        self.dataSet = None
        if fileName is not None:
            if self.Verbose: print(' Loading DataSet',fileName)
            result = self.loadDataSet(fileName)
        if result:
            self.customerSize = len(self.data['CustomerID'].unique())
            self.numItem = len(self.data['StockCode'].unique())
            self.numStorage = numStorage
            self.numInvoice = len(self.data['InvoiceNo'].unique())
            self.numDC = numDC
            self.Longitude_Base = -1.258922
            self.Latitude_Base = 51.749524
            self.fileName_CustomerLocation = './data/CustomerLocation.pkl'
            self.fileName_ProductStorage = './data/ProductStorage.pkl'
            self.fileName_DCLocation = './data/DCLocation.pkl'
            self.fileName_InvoiceList = './data/InvoiceList.pkl'
            self.fileName_StorageLocation = './data/StorageLocation.pkl'
            self.fileName_TopicList = './data/TopicList.pkl'
            self.setup()
    def loadDataSet(self, fileName = None):
        if(fileName is None):
            raise ValueError("DataSet.loadDataSet: No file is provided.")
        if(type(fileName) is not str):
            raise ValueError("DataSet.loadDataSet: fileName must be a string.")
        if(len(fileName) < 4):
            raise ValueError("DataSet.loadDataSet: Input file name is too short.")
        if(not os.path.isfile(fileName)):
            raise ValueError("DataSet.loadDataSet: File is not found.")
        self.dataSet = sio.loadmat(fileName)
        d = self.dataSet['data']
        InvoiceNo = d['InvoiceNo'][0][0][0]
        StockCode = d['StockCode'][0][0][0]
        CustomerID =d['CustomerID'][0][0][0]
        Quantity = d['Quantity'][0][0][0]
        self.data = pd.DataFrame({'InvoiceNo':InvoiceNo,'StockCode':StockCode,'CustomerID':CustomerID,'Quantity':Quantity})
        if self.Verbose: print('Successfully Load Data Set')
        return True
    def getData(self):
        return self.data
    def getOrder(self):
        return self.dataSet['m_order']
    def setup(self):
        self.generateCustomerLocation(customerSize = self.customerSize, Longitude_Base = self.Longitude_Base, Latitude_Base = self.Latitude_Base, scale = 0.6)
        self.generateProductStorage(numItem = self.numItem,numStorage = self.numStorage)
        self.generateInvoiceList(numInvoice = self.numInvoice)
        self.generateDCLocation(numDC = self.numDC, Longitude_Base = self.Longitude_Base, Latitude_Base = self.Latitude_Base)
        self.generateStorageLocation(numStorage = self.numStorage, Longitude_Base = self.Longitude_Base, Latitude_Base = self.Latitude_Base)
        self.generateTopicList(numStorage = self.numStorage)
    def generateDCLocation(self,numDC = 20, Longitude_Base = 0, Latitude_Base = 0):
        if not os.path.isfile(self.fileName_DCLocation):
            DCLocation = np.random.normal(loc = 0.5,scale = 0.13, size = (numDC,2))
            DCLongtitude = DCLocation[:,0] + Longitude_Base
            DCLatitude = DCLocation[:,1] + Latitude_Base
            self.DCLocation = np.column_stack((DCLongtitude, DCLatitude))
            with open(self.fileName_DCLocation, 'wb') as handle:
                cPickle.dump(self.DCLocation, handle)
            if self.Verbose: print("Successfully Generate Distribution Centers Location")
        else:
            # Load the file
            with open(self.fileName_DCLocation, 'rb') as handle:
                self.DCLocation = cPickle.load(handle)
            if self.Verbose: print("Successfully Load Customer Location")
    def generateCustomerLocation(self, customerSize, Longitude_Base = 0, Latitude_Base = 0, scale = 1):
        if not os.path.isfile(self.fileName_CustomerLocation):
            # Generate Customer Location if the file doesn't exist
            customerLocation = np.random.normal(loc = 0,scale = scale, size = (customerSize,2))
            customerLongtitude = customerLocation[:,0] + Longitude_Base
            customerLatitude = customerLocation[:,1] + Latitude_Base
            self.customerLocation = np.column_stack((customerLongtitude, customerLatitude))
            with open(self.fileName_CustomerLocation, 'wb') as handle:
                cPickle.dump(self.customerLocation, handle)
            if self.Verbose: print("Successfully Generate Customer Location")
        else:
            # Load the file
            with open(self.fileName_CustomerLocation, 'rb') as handle:
                self.customerLocation = cPickle.load(handle)
            if self.Verbose: print("Successfully Load Customer Location")
    def generateProductStorage(self,numItem,numStorage):
        if not os.path.isfile(self.fileName_ProductStorage):
            # Generate ProductStorage if the file doesn't exist
            productStorage = np.zeros((numItem,2), dtype=int)
            for i in range(numItem):
                storageNum = np.random.choice(np.arange(numStorage))
                productStorage[i] = [i,storageNum]
            self.productStorage = productStorage
            with open(self.fileName_ProductStorage, 'wb') as handle:
                cPickle.dump(self.productStorage, handle)
            if self.Verbose: print("Successfully Product Storage")
        else:
            # Load the file
            with open(self.fileName_ProductStorage, 'rb') as handle:
                self.productStorage = cPickle.load(handle)
            if self.Verbose: print("Successfully Load Product Storage")
    def generateInvoiceList(self,numInvoice):
        if not os.path.isfile(self.fileName_InvoiceList):
            # Generate InvoiceList if the file doesn't exist
            data = self.getData()
            InvoiceList = [{} for _ in range(numInvoice)]
            for index, row in data.iterrows():
                CustomerID, InvoiceNo, Quantity, StockCode = row
                if StockCode not in InvoiceList[InvoiceNo]:
                    InvoiceList[InvoiceNo][StockCode] = Quantity
                else:
                    InvoiceList[InvoiceNo][StockCode] += Quantity
                if 'CustomerID' not in InvoiceList[InvoiceNo]:
                    InvoiceList[InvoiceNo]['CustomerID'] = CustomerID
            self.invoiceList = InvoiceList
            with open(self.fileName_InvoiceList, 'wb') as handle:
                cPickle.dump(self.invoiceList, handle)
            if self.Verbose: print("Successfully Generate Mapping (InvoiceNo to StockCode)")
        else:
            # Load the file
            with open(self.fileName_InvoiceList, 'rb') as handle:
                self.invoiceList = cPickle.load(handle)
            if self.Verbose: print("Successfully Load Mapping (InvoiceNo to StockCode)")
    def generateStorageLocation(self,numStorage = 6, Longitude_Base = 0, Latitude_Base = 0):
        if not os.path.isfile(self.fileName_StorageLocation):
            # Generate StorageLocation if the file doesn't exist
            storageLocation = np.array([[0.912,0.471],[0.765,0.824],[0.295,0.835],[0.165,0.524],[0.341,0.241],[0.753,0.247]])
            storageLongtitude = storageLocation[:,0] + Longitude_Base
            storageLatitude = storageLocation[:,1] + Latitude_Base
            self.storageLocation = np.column_stack((storageLongtitude, storageLatitude))
            with open(self.fileName_StorageLocation, 'wb') as handle:
                cPickle.dump(self.storageLocation, handle)
            if self.Verbose: print("Successfully Generate Storage Location")
        else:
            # Load the file
            with open(self.fileName_StorageLocation, 'rb') as handle:
                self.storageLocation = cPickle.load(handle)
            if self.Verbose: print("Successfully Load Storage Location")
    def generateTopicList(self,numStorage = 6):
        # Generate TopicList if the file doesn't exist
        if not os.path.isfile(self.fileName_TopicList):
            TopicList = []
            invoiceList = self.invoiceList
            customerLocation = self.customerLocation
            productStorage = self.productStorage
            for invoice in invoiceList:
                customerID = invoice['CustomerID']
                longitude = customerLocation[customerID][0]
                latitude = customerLocation[customerID][1]
                location = [longitude,latitude]
                # there are only 6 stores
                count = [0 for i in range(numStorage)]
                for stockCode in invoice:
                    if stockCode != 'CustomerID':
                        storageNum = productStorage[stockCode][1]
                        count[storageNum] += invoice[stockCode]
                record = count + location
                TopicList.append(record)
            self.topicList = TopicList
            with open(self.fileName_TopicList, 'wb') as handle:
                cPickle.dump(self.topicList, handle)
            if self.Verbose: print("Successfully Generate Topic List")
        else:
            # Load the file
            with open(self.fileName_TopicList, 'rb') as handle:
                self.topicList = cPickle.load(handle)
            if self.Verbose: print("Successfully Load Topic List")
