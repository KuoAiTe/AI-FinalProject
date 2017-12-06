'''
provide some functions
'''
import numpy as np

def calDistance(point1, point2):
    '''
    calculate distance between point1 and point2
    point should be a list with format: wh1, wh2, ..., whM, location_x, location_y
    '''
    d = np.linalg.norm(np.array(point1) - np.array(point2))
    return d 
    