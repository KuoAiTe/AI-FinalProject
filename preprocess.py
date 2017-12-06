import sys
import random
import math
from dataSet import dataSet
import numpy as np
import pandas as pd

class preprocessor():
    def __init__(self, fileName):
        self.df = dataSet(fileName)
        self.data = self.df.getData()

    def get_order(self):
        m_order = self.df.getOrder()
        # print(data)
        print(m_order[0,0])
        print(m_order[7,0])
        print(m_order[1,0])
        
        return m_order

