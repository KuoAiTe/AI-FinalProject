'''
provide some functions
'''
import math
import numpy as np

def calDistance(point1, point2):
    '''
    Calculate distance between point1 and point2.
    Point should be a list with format: wh1, wh2, ..., whM, location_x, location_y.
    Similarity of items should be weighted by ALPHA, and that of location should be weighted by BEAT.
    '''

    ALPHA = 0.5
    BETA = 0.5

    front_point1 = point1[0:(len(point1) - 2)]
    back_point1 = point1[(len(point1) - 2):len(point1)]
    front_point2 = point2[0:(len(point2) - 2)]
    back_point2 = point2[(len(point2) - 2):len(point2)]

    d1 = np.linalg.norm(np.array(front_point1) - np.array(front_point2))
    d2 = np.linalg.norm(np.array(back_point1) - np.array(back_point2))
    d = ALPHA * d1 + BETA * d2

    # d = np.linalg.norm(np.array(point1) - np.array(point2))
    return d 
    

def calObjective(quantityTopic, quantityInvoice, w_location, d_location, c_location, idx):
    '''calculate the objective value'''
    # all arguments should be numpy objects
    # m_quantity: matrix of orders, each record is an order, containing the number of each iterm (order * item)
    # m_skuKeeping: matrix of types of SKU kept in warehouses (warehouse * item)
    # w_location, d_location, c_location: positions of warehouses, distribution centers, and customers
    # m_nearWarehouse: matrix of the warehouse for each distribution center sorting by distance (warehouse * dc)
    # m_clusters: set of orders within each cluster
    # m_ocPair: indicate the customer placing each order
    # m_allocation: assignment of orders to distribution centers
    
    # capacity_truck = 1
    # num_warehouse = len(w_location)
    # num_dc = len(d_location)
    # num_customer = len(c_location)
    # num_order = quantity.shape[0]
    # num_item = quantity.shape[1]

    # num_truck = np.zeros(((len(clusters), len(nearWarehouse[0]))), dtype = int)
    # travelDist_dw = 0
    # travelDist_do = 0
    # for k in range(num_dc):
    #     travelDist_dw_per_dc = 0
    #     itemSum = []
    #     for i in range(len(clusters[k])):        # loop in each cluster
    #         itemSum += quantity[clusters[k][i]]
    #     sum = np.sum(itemSum)
    #     sum_warehouse = np.zeros(num_warehouse)
    #     for j in range(num_warehouse):
    #         if sum == 0:
    #             break
    #         else:
    #             for t in range(num_item):
    #                 if skuKeeping[nearWarehouse[k][j]][t] == 1:
    #                     sum_warehouse += itemSum[t]
    #                     sum -= itemSum[t]
    #             num = math.ceil(sum_warehouse / capacity_truck)
    #         # travelDist_dw_per_dc += m_distDW[k][j] * num
    #         travelDist_dw_per_dc += calDistance(d_location[k], w_location[j]) * num
    #     travelDist_dw += travelDist_dw_per_dc
    
    #     travelDist_do_per_dc = 0
    #     indicator = np.zeros(num_customer)
    #     for i in range(len(clusters[k])):
    #         customerID = ocPair[clusters[k][i]]
    #         if indicator[customerID] == 0:
    #             # travelDist_do_per_dc += m_distDO[k][customerID]
    #             travelDist_do_per_dc += calDistance(d_location[k], c_location[customerID])
    #             indicator[customerID] = 1
    #     travelDist_do += travelDist_do_per_dc

    num_order = len(quantityTopic)
    num_warehouse = len(w_location)
    num_customer = len(c_location)
    travelDist_dw = 0
    travelDist_dc = 0
    c1 = 1.0
    c2 = 2.0
    cost = 0
    for i in range(num_order):
        totQuantity = 0
        customerID = quantityInvoice[i]['CustomerID']
        for k in range(num_warehouse):
            travelDist_dw += calDistance(d_location[idx[i]], w_location[k]) * quantityTopic[i][k]
            totQuantity += quantityTopic[i][k]
        travelDist_dc += totQuantity * calDistance(d_location[idx[i]], c_location[customerID])
    
    cost += c1 * travelDist_dc + c2 * travelDist_dw
    return cost