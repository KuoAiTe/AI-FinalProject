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
class preProcessor():
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
            if self.Verbose: print('Dataset is loaded.')
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
        if self.Verbose: print('Load Data Set')
        return True
    def getData(self):
        return self.data
    def getOrder(self):
        return self.dataSet['m_order']
    def setup(self):
        self.generateInvoiceList(numInvoice = self.numInvoice)
        self.generateCustomerLocation(customerSize = self.customerSize, Longitude_Base = self.Longitude_Base, Latitude_Base = self.Latitude_Base, scale = 0.6)
        self.generateProductStorage(numItem = self.numItem,numStorage = self.numStorage)
        self.generateStorageLocation(numStorage = self.numStorage, Longitude_Base = self.Longitude_Base, Latitude_Base = self.Latitude_Base)
        self.generateDCLocation(numDC = self.numDC, Longitude_Base = self.Longitude_Base, Latitude_Base = self.Latitude_Base)
        self.generateDistanceBetweenStorageAndDC(numDC = self.numDC,numStorage = self.numStorage)
        self.generateLeastDistance(numDC = self.numDC)
        self.generateTopicList(numStorage = self.numStorage)
        self.generateNormalizedTopicList(numInvoice = self.numInvoice, numStorage = self.numStorage)

    def getCustomerLocation(self):
        '''
        return: <type 'numpy.ndarray'>
        '''
        if self.Verbose: print('getCustomerLocation()',type(self.CustomerLocation))
        return self.CustomerLocation
    def getProductStorage(self):
        '''
        return: <type 'numpy.ndarray'>
        '''
        if self.Verbose: print('getProductStorage()',type(self.ProductStorage))
        return self.ProductStorage
    def getInvoiceList(self):
        '''
        return: <type 'list'>
        '''
        if self.Verbose: print('getInvoiceList()',type(self.ProductStorage))
        return self.InvoiceList
    def getStorageLocation(self):
        '''
        return: <type 'numpy.ndarray'>
        '''
        if self.Verbose: print('getStorageLocation()',type(self.StorageLocation))
        return self.StorageLocation
    def getDC(self):
        '''
        return: <type 'numpy.ndarray'>
        '''
        if self.Verbose: print('getDC()',type(self.DCLocation))
        return self.DCLocation
    def getTopicList(self):
        '''
        return: <type 'list'>
        '''
        if self.Verbose: print('getTopicList()',type(self.TopicList))
        return self.TopicList
    def getNormalizedTopicList(self):
        '''
        return: <type 'list'>
        '''
        if self.Verbose: print('getNormalizedTopicList()',type(self.NormalizedTopicList))
        return self.NormalizedTopicList
    def getDistance(self):
        '''
        return: <type 'numpy.ndarray'>
        '''
        if self.Verbose: print('getDistance',type(self.Distance_DC_Storage))
        return self.Distance_DC_Storage
    def getSortedDistanceIndex(self):
        '''
        return: <type 'list'>
        '''
        if self.Verbose: print('getSortedDistanceIndex()',type(self.SortedDistanceIndex))
        return self.SortedDistanceIndex
    def generateLeastDistance(self,numDC = 20):
        SortedDistanceIndex = []
        for i in range(numDC):
            record = self.Distance_DC_Storage[i]
            _sort = np.argsort(record)
            SortedDistanceIndex.append(_sort)
        self.SortedDistanceIndex = SortedDistanceIndex
    def generateDistanceBetweenStorageAndDC(self,numStorage =6, numDC=20):
        # Generate Distance Between Each Storage And Distribution Center
        DC = self.DCLocation
        StorageLocation = self.StorageLocation
        distance = np.zeros((numDC,numStorage))
        for i in range(numDC):
            dc = DC[i]
            for j in range(numStorage):
                storage = StorageLocation[j]
                distance[i,j] = np.linalg.norm(dc-storage)
        self.Distance_DC_Storage = distance
    def generateDCLocation(self,numDC = 20, Longitude_Base = 0, Latitude_Base = 0):
        if not os.path.isfile(self.fileName_DCLocation):
            # Generate DCLocation if the file doesn't exist
            DCLocation = np.random.normal(loc = 0.5,scale = 0.13, size = (numDC,2))
            DCLongtitude = DCLocation[:,0] + Longitude_Base
            DCLatitude = DCLocation[:,1] + Latitude_Base
            self.DCLocation = np.column_stack((DCLongtitude, DCLatitude))
            with open(self.fileName_DCLocation, 'wb') as handle:
                cPickle.dump(self.DCLocation, handle)
            if self.Verbose: print("Generate Distribution Centers Location",self.fileName_DCLocation)
        else:
            # Load the file
            with open(self.fileName_DCLocation, 'rb') as handle:
                self.DCLocation = cPickle.load(handle)
            if self.Verbose: print("Load Customer Location",self.fileName_DCLocation)
    def generateCustomerLocation(self, customerSize, Longitude_Base = 0, Latitude_Base = 0, scale = 1):
        if not os.path.isfile(self.fileName_CustomerLocation):
            # Generate Customer Location if the file doesn't exist
            customerLocation = np.random.normal(loc = 0,scale = scale, size = (customerSize,2))
            customerLongtitude = customerLocation[:,0] + Longitude_Base
            customerLatitude = customerLocation[:,1] + Latitude_Base
            self.CustomerLocation = np.column_stack((customerLongtitude, customerLatitude))
            with open(self.fileName_CustomerLocation, 'wb') as handle:
                cPickle.dump(self.CustomerLocation, handle)
            if self.Verbose: print("Generate Customer Location",self.fileName_CustomerLocation)
        else:
            # Load the file
            with open(self.fileName_CustomerLocation, 'rb') as handle:
                self.CustomerLocation = cPickle.load(handle)
            if self.Verbose: print("Load Customer Location",self.fileName_CustomerLocation)
    def generateProductStorage(self,numItem,numStorage):
        if not os.path.isfile(self.fileName_ProductStorage):
            # Generate ProductStorage if the file doesn't exist
            productStorage = np.zeros((numItem,2), dtype=int)
            for i in range(numItem):
                storageNum = np.random.choice(np.arange(numStorage))
                productStorage[i] = [i,storageNum]
            self.ProductStorage = productStorage
            with open(self.fileName_ProductStorage, 'wb') as handle:
                cPickle.dump(self.ProductStorage, handle)
            if self.Verbose: print("Product Storage",self.fileName_ProductStorage)
        else:
            # Load the file
            with open(self.fileName_ProductStorage, 'rb') as handle:
                self.ProductStorage = cPickle.load(handle)
            if self.Verbose: print("Load Product Storage",self.fileName_ProductStorage)
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
            self.InvoiceList = InvoiceList
            with open(self.fileName_InvoiceList, 'wb') as handle:
                cPickle.dump(self.InvoiceList, handle)
            if self.Verbose: print("Generate Mapping (InvoiceNo to StockCode)",self.fileName_InvoiceList)
        else:
            # Load the file
            with open(self.fileName_InvoiceList, 'rb') as handle:
                self.InvoiceList = cPickle.load(handle)
            if self.Verbose: print("Load Mapping (InvoiceNo to StockCode)",self.fileName_InvoiceList)
    def generateStorageLocation(self,numStorage = 6, Longitude_Base = 0, Latitude_Base = 0):
        if not os.path.isfile(self.fileName_StorageLocation):
            # Generate StorageLocation if the file doesn't exist
            storageLocation = np.array([[0.912,0.471],[0.765,0.824],[0.295,0.835],[0.165,0.524],[0.341,0.241],[0.753,0.247]])
            storageLongtitude = storageLocation[:,0] + Longitude_Base
            storageLatitude = storageLocation[:,1] + Latitude_Base
            self.StorageLocation = np.column_stack((storageLongtitude, storageLatitude))
            with open(self.fileName_StorageLocation, 'wb') as handle:
                cPickle.dump(self.storageLocation, handle)
            if self.Verbose: print("Generate Storage Location",self.fileName_StorageLocation)
        else:
            # Load the file
            with open(self.fileName_StorageLocation, 'rb') as handle:
                self.StorageLocation = cPickle.load(handle)
            if self.Verbose: print("Load Storage Location",self.fileName_StorageLocation)
    def generateTopicList(self,numStorage = 6):
        # Generate TopicList if the file doesn't exist
        if not os.path.isfile(self.fileName_TopicList):
            TopicList = []
            invoiceList = self.InvoiceList
            customerLocation = self.CustomerLocation
            productStorage = self.ProductStorage
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
            self.TopicList = TopicList
            with open(self.fileName_TopicList, 'wb') as handle:
                cPickle.dump(self.topicList, handle)
            if self.Verbose: print("Generate Topic List",self.fileName_TopicList)
        else:
            # Load the file
            with open(self.fileName_TopicList, 'rb') as handle:
                self.TopicList = cPickle.load(handle)
            if self.Verbose: print("Load Topic List",self.fileName_TopicList)
    def generateNormalizedTopicList(self,numInvoice = 16649, numStorage = 6):
        #for invoice in self.TopicList:
        #    print(invoice)
        NormalizedTopicList = self.TopicList[:]
        for i in range(numInvoice):
            invoice = NormalizedTopicList[i]
            denominator = sum(invoice[0:numStorage])
            for j in range(numStorage):
                invoice[j] /= denominator *1.0
        self.NormalizedTopicList = NormalizedTopicList
