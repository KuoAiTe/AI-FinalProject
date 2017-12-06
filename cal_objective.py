'''calculate the objective value'''
import math
import numpy as np

def cal_objective(m_quantity, m_skuKeeping, m_distDW, m_distDO, capacity_truck, m_nearWarehouse, m_allocation):
    # all arguments should be numpy objects
    # m_quantity: matrix of orders, each record is an order, containing the number of each iterm (order * item)
    # m_skuKeeping: matrix of types of SKU kept in warehouses (warehouse * item)
    # m_distDW: matrix of distances between distribution centers and warehouses (dc * warehouse)
    # m_distDO: matrix of distances between distribution cneters and customer placing order (dc * order)
    # capacity_truck: capacity of trucks of different types
    # m_accomadate: matrix of accomadation of item to type of truck (item * type)
    # m_nearWarehouse: matrix of the warehouse for each distribution center sorting by distance (warehouse * dc)
    # m_allocation: assignment of orders to distribution centers
    
    num_warehouse = m_skuKeeping.shape[0]
    num_dc = m_distDW.shape[0]
    num_order = m_quantity.shape[0]
    num_item = m_quantity.shape[1]
    # quantity = np.arange(num_order*num_item).reshape((num_order, num_item))     # quantity of item t in order i
    # capacity = np.arange(num_trucktype)                                              # capacity of truck of type h
    # check_warehouse = np.arange(num_warehouse*num_item*num_dc).reshape((num_warehouse, num_item, num_dc))   # whether warehouse j is the nearest one with SKU t for distribution center k
    # dist_dw = np.arange(num_dc*num_warehouse).reshape((num_dc, num_warehouse))     # distance between distribution and warehouse
    # dist_do = np.arange(num_dc*num_order).reshape((num_dc, num_order))             # distance between distribution and customer placing order i

    # allocation = np.arange(num_order*num_dc).reshape((num_order, num_dc))       # assignment of orders to distribution centers

    travelDist = 0
    for k in range(0, num_dc):
        travelDist_dw_per_dc = 0        # the cost generated bteween a dc and warehouses
        for j in range(0, num_warehouse):   # ordering number of warehouses for dc k, not warehouse ID
            num_truck = 0
            sum_item = 0
            for i in range(0, num_order):
                for t in range(0, num_item):
                    sum_item = sum_item + m_quantity(i, t) * m_skuKeeping(m_nearWarehouse(k, j), t) * m_allocation(i, k)
                    m_quantity(i, t) = 0    # avoid repeated calculating
            num_truck = num_truck + math.ceil(sum_item / capacity_truck)
            travelDist_dw_per_dc = travelDist_dw_per_dc + num_truck * m_distDW(k, m_nearWarehouse(k, j))

        travelDist_do_per_dc = 0        # the cost generated bteween a dc and customers placing order
        for i in range(0, num_order):
            travelDist_do_per_dc = travelDist_do_per_dc + m_distDO(k, i) * m_allocation(i, k)

        travelDist = travelDist + travelDist_dw_per_dc + travelDist_do_per_dc

    print(travelDist)
    return travelDist


        