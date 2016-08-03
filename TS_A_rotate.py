#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import math
import TS_functions

## Total Station Line A

TS_data_file= '/Users/jasondec/0_gradwork/0_hcf/TS_A_v0.csv'
GPS_data_file = '/Users/jasondec/0_gradwork/0_hcf/GPS_A_v0.csv'
TS_data = pd.read_csv(TS_data_file)
GPS_data = pd.read_csv(GPS_data_file)
# print data

def rotate(xPoint,yPoint,x0,y0,angle):
    import math

    xDiff = xPoint - x0
    yDiff = yPoint - y0
    xNew = x0 + xDiff * math.cos(angle) - xDiff * math.sin(angle)
    yNew = y0 + yDiff * math.cos(angle) + yDiff * math.sin(angle)
    return xNew,yNew


## Correct TS Line A data by rotating 180 deg
angle = 180 #degrees
xBase = TS_data.loc[0]['X0']      # x-coord of baseA
yBase = TS_data.loc[0]['Y0']      # y-coord of baseA

TS_data['X1'],TS_data['Y1'] = rotate(TS_data['X0'],TS_data['Y0'],xBase,yBase,angle * math.pi/180)
# print TS_data

angle = 7
print rotate(TS_data['X1'],TS_data['Y0'],xBase,yBase,angle * math.pi/180)

