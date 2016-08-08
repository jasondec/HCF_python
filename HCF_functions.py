#!/Users/jasondec/anaconda2/bin/python

def rotate_xy(xPoint,yPoint,x0,y0,angle):
    import math

    xDiff = xPoint - x0
    yDiff = yPoint - y0
    xNew = x0 + xDiff * math.cos(angle) - yDiff * math.sin(angle)
    yNew = y0 + yDiff * math.cos(angle) + xDiff * math.sin(angle)
    return xNew,yNew

def calc_misfit(x1,y1,x2,y2):
    import numpy as np

    delX = abs(x1 - x2)
    delY = abs(y1 - y2)
    out = np.sqrt(np.square(delX) + np.square(delY))
    return out
