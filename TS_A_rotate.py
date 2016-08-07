#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from HCF_functions import rotate_xy,calc_misfit

## Total Station Line A

TS_data_file= '/Users/jasondec/0_gradwork/0_hcf/TS_A_v0.csv'
GPS_data_file = '/Users/jasondec/0_gradwork/0_hcf/GPS_A_v0.csv'
TS_data = pd.read_csv(TS_data_file)
GPS_data = pd.read_csv(GPS_data_file)


## copy original values to new working columns
TS_data['x_working'] = TS_data['X0']
TS_data['y_working'] = TS_data['Y0']
TS_data['z_working'] = TS_data['Z0']

## Plot raw points
plt.scatter(TS_data['x_working'],TS_data['y_working'], color='grey')
plt.scatter(GPS_data['Lon'],GPS_data['Lat'], color='orange')



## Find base points in TS and GPS tables
# A_base_GPS = GPS_data.loc[GPS_data['Point'] == 'A_base']
# A_base_TS = TS_data.loc[TS_data['ID'] == 'A_base']
A_base_TS_key = 0
A_base_GPS_key = 7


## Shift all TS points by A_base_GPS - A_base_TS in x,y,z
A_base_GPS = GPS_data.loc[A_base_GPS_key]
A_base_TS = TS_data.loc[A_base_TS_key]

delX = A_base_GPS['Lon'] - A_base_TS['X0']
delY = A_base_GPS['Lat'] - A_base_TS['Y0']
delZ = A_base_GPS['Elev'] - A_base_TS['Z0']

TS_data['x_working'] = TS_data['x_working'] + delX
TS_data['y_working'] = TS_data['y_working'] + delY
TS_data['z_working'] = TS_data['z_working'] + delZ

## Plot shifted points
plt.scatter(TS_data['x_working'],TS_data['y_working'], color='blue')



## Correct TS Line A data by rotating 180 deg
angle = 180 #degrees
xBase = TS_data.loc[A_base_TS_key]['x_working']      # x-coord of baseA
yBase = TS_data.loc[A_base_TS_key]['y_working']      # y-coord of baseA

TS_data['x_working'],TS_data['y_working'] = rotate_xy(TS_data['x_working'],TS_data['y_working'],xBase,yBase,angle * math.pi/180)

## Plot rotated points
plt.scatter(TS_data['x_working'],TS_data['y_working'], color='red')
# plt.show()


## ID co-located GPS and TS points by index
for point in ['A_001']:
    x1 = GPS_data.loc[GPS_data['Point'] == point]['Lon']
    y1 = GPS_data.loc[GPS_data['Point'] == point]['Lat']
    x2 = TS_data.loc[TS_data['ID'] == point]['x_working']
    y2 = TS_data.loc[TS_data['ID'] == point]['y_working']
    print x1
    print y1
    print x2
    print y2
    # misfit = calc_misfit(x1,y1,x2,y2)
    delX = abs(x1 - x2)
    delY = abs(y1 - y2)
    # off = math.sqrt(delX ^ 2 + delY ^ 2)
    off = (delX^2 + delY^2)
    print off
