import sys
import random
import math
from dataSet import dataSet
import numpy as np
import pandas as pd

class preprocessor():
    def __init__(self, fileName):
        self.df = dataSet(fileName)
        # self.CustomerLocation = self.df.getCustomerLocation()
        # self.ProductStorage = self.df.getProductStorage()
        # self.InvoiceList = self.df.getInvoiceList()

    def get_order(self):
        # return self.df.getTopicList()
        return self.df.getNormalizedTopicList()

    def get_wLocation(self):
        return self.df.getStorageLocation()

    def get_dLocation(self):
        return self.df.getDC()

    def get_sortedWarehouses(self):
        return self.df.getDistance()

    def get_invoiceList(self):
        return self.df.getInvoiceList()

    def get_productStorage(self):
        return self.df.getProductStorage()

    def get_cLocation(self):
        return self.df.getCustomerLocation()

    def get_sortedDistanceIndex(self):
        return self.df.getSortedDistanceIndex()

    def get_topicList(self):
        return self.df.getTopicList()

    def get_skuKeeing(self):
        return self.df.getProductStorage()

    def get_quantity(self):
        return self.df.getInvoiceList()
