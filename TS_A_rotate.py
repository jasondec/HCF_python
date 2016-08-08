#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
import numpy as np
import scipy.optimize as optimization
import matplotlib.pyplot as plt
import math


from HCF_functions import rotate_xy, calc_misfit

## Total Station Line A

TS_data_file = '/Users/jasondec/0_gradwork/0_hcf/TS_A_v0.csv'
GPS_data_file = '/Users/jasondec/0_gradwork/0_hcf/GPS_A_v0.csv'
TS_data = pd.read_csv(TS_data_file, index_col='ID')  ## import CSV file using ID col as the indexer
GPS_data = pd.read_csv(GPS_data_file, index_col='gps_point')  ## import CSV file using Point col as indexer
df = pd.merge(TS_data, GPS_data, left_index=True, right_index=True, how='left')

## copy original values to new working columns
df['x_working'] = df['X0']
df['y_working'] = df['Y0']
df['z_working'] = df['Z0']

## Plot raw points
plt.scatter(df['x_working'], df['y_working'], color='grey')
plt.scatter(df['gps_lon'], df['gps_lat'], color='orange')

## Shift all TS points by A_base_GPS - A_base_TS in x,y,z

delX = df.loc['A_base']['gps_lon'] - df.loc['A_base']['X0']
delY = df.loc['A_base']['gps_lat'] - df.loc['A_base']['Y0']
delZ = df.loc['A_base']['gps_elev'] - df.loc['A_base']['Z0']

df['x_working'] = df['x_working'] + delX
df['y_working'] = df['y_working'] + delY
df['z_working'] = df['z_working'] + delZ

## Plot shifted points
plt.scatter(df['x_working'], df['y_working'], color='blue')

## Correct TS Line A data by rotating 180 deg.  Not applicable to other lines.
angle = 180  # degrees
xBase = df.loc['A_base']['x_working']  # x-coord of baseA
yBase = df.loc['A_base']['y_working']  # y-coord of baseA

df['x_working'], df['y_working'] = rotate_xy(df['x_working'], df['y_working'], xBase, yBase, angle * math.pi / 180)  ## rotate using external fcn


## Plot rotated points
plt.scatter(df['x_working'], df['y_working'], color='red')

# ## Rotate arbitry angle
# angle = 2  # degrees
# xBase = df.loc['A_base']['x_working']  # x-coord of baseA
# yBase = df.loc['A_base']['y_working']  # y-coord of baseA
#
# df['x_working'], df['y_working'] = rotate_xy(df['x_working'], df['y_working'], xBase, yBase, angle * math.pi / 180)  ## rotate using external fcn
# plt.scatter(df['x_working'], df['y_working'], color='yellow')
#
# plt.show()
#
# exit()


def calc_chisqr(df):
    ## calculate chi-square for each point (chisqr X + chisqrY)
    df['chi_sqr'] = np.square(df['x_working'] - df['gps_lon']) / df['x_working'] + np.square(df['y_working'] - df['gps_lat']) / df['y_working']
    ## weight misfit by inverse of gps accuracy
    df['misfit'] = df['chi_sqr'] / df['gps_horiz_acc']
    return df

def rotate_ang(df,angle):   ## angle in degrees
    import math
    import numpy as np

    df['x_working'], df['y_working'] = rotate_xy(df['x_working'], df['y_working'], xBase, yBase, angle * math.pi / 180)
    plt.scatter(df['x_working'], df['y_working'], color='yellow')
    df = calc_chisqr(df)
    return df['misfit'].sum()

rotate_ang(df,-9)
plt.show()
# print df
exit()
