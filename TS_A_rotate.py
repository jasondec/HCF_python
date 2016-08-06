#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import math

## Total Station Line A

TS_data_file= '/Users/jasondec/0_gradwork/0_hcf/TS_A_v0.csv'
GPS_data_file = '/Users/jasondec/0_gradwork/0_hcf/GPS_A_v0.csv'
TS_data = pd.read_csv(TS_data_file)
GPS_data = pd.read_csv(GPS_data_file)

def rotate_xy(xPoint,yPoint,x0,y0,angle):
    import math

    xDiff = xPoint - x0
    yDiff = yPoint - y0
    xNew = x0 + xDiff * math.cos(angle) - xDiff * math.sin(angle)
    yNew = y0 + yDiff * math.cos(angle) + yDiff * math.sin(angle)
    return xNew,yNew

## copy original values to new working columns
TS_data['x_working'] = TS_data['X0']
TS_data['y_working'] = TS_data['Y0']
TS_data['z_working'] = TS_data['Z0']

## Find base points in TS and GPS tables
# A_base_GPS = GPS_data.loc[GPS_data['Point'] == 'A_base']
# A_base_TS = TS_data.loc[TS_data['ID'] == 'A_base']
A_base_GPS = GPS_data.loc[7]
A_base_TS = TS_data.loc[0]


## Shift all TS points by A_base_GPS - A_base_TS in x,y,z
delX = A_base_GPS['Lon'] - A_base_TS['X0']
delY = A_base_GPS['Lat'] - A_base_TS['Y0']
delZ = A_base_GPS['Elev'] - A_base_TS['Z0']
print delX, delY, delZ

TS_data['x_working'] = TS_data['x_working'] + delX
TS_data['y_working'] = TS_data['y_working'] + delY
TS_data['z_working'] = TS_data['z_working'] + delZ

print TS_data

## Correct TS Line A data by rotating 180 deg
angle = 180 #degrees
xBase = TS_data.loc[0]['X0']      # x-coord of baseA
yBase = TS_data.loc[0]['Y0']      # y-coord of baseA


TS_data['X1'],TS_data['Y1'] = rotate_xy(TS_data['X0'],TS_data['Y0'],xBase,yBase,angle * math.pi/180)
# print TS_data

angle = 7
# print rotate_xy(TS_data['X1'],TS_data['Y0'],xBase,yBase,angle * math.pi/180)

