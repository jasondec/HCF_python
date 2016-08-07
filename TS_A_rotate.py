#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from HCF_functions import rotate_xy,calc_misfit

## Total Station Line A

TS_data_file= '/Users/jasondec/0_gradwork/0_hcf/TS_A_v0.csv'
GPS_data_file = '/Users/jasondec/0_gradwork/0_hcf/GPS_A_v0.csv'
TS_data = pd.read_csv(TS_data_file, index_col='ID')         ## import CSV file using ID col as the indexer
GPS_data = pd.read_csv(GPS_data_file, index_col='Point')    ## import CSV file using Point col as indexer
# df = pd.merge(TS_data,GPS_data, left_index=True,right_index=True, how='left')
# print df

## copy original values to new working columns
TS_data['x_working'] = TS_data['X0']
TS_data['y_working'] = TS_data['Y0']
TS_data['z_working'] = TS_data['Z0']

## Plot raw points
plt.scatter(TS_data['x_working'],TS_data['y_working'], color='grey')
plt.scatter(GPS_data['Lon'],GPS_data['Lat'], color='orange')


## Shift all TS points by A_base_GPS - A_base_TS in x,y,z
A_base_GPS = GPS_data.loc['A_base']
A_base_TS = TS_data.loc['A_base']

delX = A_base_GPS['Lon'] - A_base_TS['X0']
delY = A_base_GPS['Lat'] - A_base_TS['Y0']
delZ = A_base_GPS['Elev'] - A_base_TS['Z0']

TS_data['x_working'] = TS_data['x_working'] + delX
TS_data['y_working'] = TS_data['y_working'] + delY
TS_data['z_working'] = TS_data['z_working'] + delZ

## Plot shifted points
plt.scatter(TS_data['x_working'],TS_data['y_working'], color='blue')



## Correct TS Line A data by rotating 180 deg.  Not applicable to other lines.
angle = 180 #degrees
xBase = TS_data.loc['A_base']['x_working']      # x-coord of baseA
yBase = TS_data.loc['A_base']['y_working']      # y-coord of baseA

TS_data['x_working'],TS_data['y_working'] = rotate_xy(TS_data['x_working'],TS_data['y_working'],xBase,yBase,angle * math.pi/180)    ## rotation function is imported

## Plot rotated points
plt.scatter(TS_data['x_working'],TS_data['y_working'], color='red')
# plt.show()


## ID co-located GPS and TS points by index
for point in ['A_001','A_016','A_030','A_045','A_060','A_080','A_095']:
    x1 = GPS_data.loc[point]['Lon']
    y1 = GPS_data.loc[point]['Lat']
    x2 = TS_data.loc[point]['x_working']
    y2 = TS_data.loc[point]['y_working']

    misfit = calc_misfit(x1,y1,x2,y2)   ## calculate misfit using external function
    TS_data.set_value(point,'misfit',misfit)
    GPS_error = GPS_data.loc[point]['Hor_Acc']

# print TS_data