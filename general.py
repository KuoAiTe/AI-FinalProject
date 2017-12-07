'''
provide some functions
'''
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
    