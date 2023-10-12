# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 12:02:18 2023

@author: Benjamin
"""

import numpy as np
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees).
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    d = c * r
    return d


def ngbStn(points, point):
    """
    Calculates neighboring points within a d <= 250 km radius.
    """
    dist = []
    ind  = []
    for i in list(range(np.shape(points)[0])):
        d = haversine(point[0], point[1], points[i][0], points[i][1])
        if d <= 250:
            dist.append(d)
            ind.append(i)
    dist = np.array(list(map(float,dist)))
    return dist, ind
            

def invDisWgt(points, grid):
    """
    - Calculates the inverted distance weight interpolation between the known points and a grid.
    - Points and grid are in decimal degrees.
    - Points have 3 columns, longitude, latitude, and the target value.
    - Grid have 2 columns, longitud and latitude.
    """
    a = list(range(np.shape(grid)[0]))
    w = []
    
    for i in a:
        dist, ind = ngbStn(points, grid[i])
        aux1 = sum(points[:,2][ind]/(dist**2))
        aux2 = sum(1/(dist**2))
        w.append(aux1/aux2)
    wgrid = np.array([grid[:,0],grid[:,1],w]).T
    return wgrid
        
            
    