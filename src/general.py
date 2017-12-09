'''
provide some functions
'''
import math
import numpy as np
import time


class Calculator:
    ALPHA = 0.5
    BETA = 0.5
    @staticmethod
    def setAlpha(i):
        Calculator.ALPHA = i
        Calculator.BETA = 1-i
    @staticmethod
    def calDistance(point1, point2):
        '''
        Calculate distance between point1 and point2.
        Point should be a list with format: wh1, wh2, ..., whM, location_x, location_y.
        Similarity of items should be weighted by ALPHA, and that of location should be weighted by BEAT.
        '''
        front_point1 = point1[:-2]
        back_point1 = point1[-2:]
        front_point2 = point2[:-2]
        back_point2 = point2[-2:]
        d1 = np.linalg.norm(front_point1 - front_point2)
        d2 = np.linalg.norm(back_point1 - back_point2)
        d = Calculator.ALPHA * d1 + Calculator.BETA * d2
        return d

    @staticmethod
    def calObjective(quantityTopic, quantityInvoice, w_location, d_location, c_location, idx):
        '''
            calculate the objective value
            all arguments should be numpy objects
            m_quantity: matrix of orders, each record is an order, containing the number of each iterm (order * item)
            m_skuKeeping: matrix of types of SKU kept in warehouses (warehouse * item)
            w_location, d_location, c_location: positions of warehouses, distribution centers, and customers
            m_nearWarehouse: matrix of the warehouse for each distribution center sorting by distance (warehouse * dc)
            m_clusters: set of orders within each cluster
            m_ocPair: indicate the customer placing each order
            m_allocation: assignment of orders to distribution centers
        '''
        num_order = len(quantityTopic)
        num_warehouse = len(w_location)
        num_customer = len(c_location)
        travelDist_dw = 0
        travelDist_dc = 0
        c1 = 2.0
        c2 = 1.0
        cost = 0
        for i in range(num_order):
            totQuantity = 0
            customerID = quantityInvoice[i]['CustomerID']
            for k in range(num_warehouse):
                dc = d_location[idx[i]]
                w = w_location[k]
                travelDist_dw += np.linalg.norm(dc - w) * quantityTopic[i][k]
                totQuantity += quantityTopic[i][k]
            travelDist_dc += totQuantity * np.linalg.norm(dc - w)

        cost += c1 * travelDist_dc + c2 * travelDist_dw
        return cost
