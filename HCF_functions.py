#!/Users/jasondec/anaconda2/bin/python

def rotate_xy(xPoint,yPoint,x0,y0,angle):
    import math

    xDiff = xPoint - x0
    yDiff = yPoint - y0
    xNew = x0 + xDiff * math.cos(angle) - xDiff * math.sin(angle)
    yNew = y0 + yDiff * math.cos(angle) + yDiff * math.sin(angle)
    return xNew,yNew

def calc_misfit(x1,y1,x2,y2):
    import math

    delX = abs(x1-x2)
    delY = abs(y1-y2)
    off = math.sqrt(delX^2 + delY^2)
    return off
