#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt

## Total Station Line A
TS_data_file = '/Users/jasondec/0_gradwork/0_hcf/TS_C_v0.csv'
GPS_data_file = '/Users/jasondec/0_gradwork/0_hcf/GPS_C_v0.csv'

def import_data(TS_data_file,GPS_data_file):
    import pandas as pd
    import matplotlib.pyplot as plt

    TS_data = pd.read_csv(TS_data_file, comment='#', index_col='ID')  ## import CSV file using ID col as the indexer
    GPS_data = pd.read_csv(GPS_data_file, comment='#', index_col='gps_point')  ## import CSV file using Point col as indexer
    df = pd.merge(TS_data, GPS_data, left_index=True, right_index=True, how='left')

    ## copy original values to new working columns
    df['x_working'] = df['X0']
    df['y_working'] = df['Y0']
    df['z_working'] = df['Z0']

    ## Plot raw points
    plt.scatter(df['x_working'], df['y_working'], color='grey')
    plt.scatter(df['gps_lon'], df['gps_lat'], color='red')

    return df

def shift_points(df,base):
    ## Shift all TS points by base - A_base_TS in x,y,z
    delX = df.loc[base]['gps_lon'] - df.loc[base]['x_working']
    delY = df.loc[base]['gps_lat'] - df.loc[base]['y_working']
    delZ = df.loc[base]['gps_elev'] - df.loc[base]['z_working']

    df['x_working'] = df['x_working'] + delX
    df['y_working'] = df['y_working'] + delY
    df['z_working'] = df['z_working'] + delZ
    return df


def rotate_points(df,angle,base):
    import math
    from HCF_functions import rotate_xy

    xBase = df.loc[base]['x_working']  # x-coord of base
    yBase = df.loc[base]['y_working']  # y-coord of base

    df['x_working'], df['y_working'] = rotate_xy(df['x_working'], df['y_working'], xBase, yBase, angle * math.pi / 180)
    return df


def calc_misfit(df):
    import numpy as np

    # ## calculate chi-square for each point (chisqr X + chisqrY)
    # df['chi_sqr'] = np.square(df['x_working'] - df['gps_lon']) / df['gps_lon'] + np.square(df['y_working'] - df['gps_lat']) / df['gps_lat']
    # ## weight misfit by inverse of gps accuracy
    # df['misfit'] = df['chi_sqr'] / df['gps_horiz_acc']

    ## calculate chi-square for each point (chisqr X + chisqrY)
    df['chi_sqr'] = np.square(df['x_working'] - df['gps_lon']) / np.square(df['gps_lon']) + np.square(df['y_working'] - df['gps_lat']) / np.square(df['gps_lat'])
    ## weight misfit by inverse of gps accuracy
    df['misfit'] = df['chi_sqr'] / df['gps_horiz_acc']
    return df


def optimize_rotation(angle):
    df = import_data('/Users/jasondec/0_gradwork/0_hcf/TS_C_v0.csv','/Users/jasondec/0_gradwork/0_hcf/GPS_C_v0.csv')  ## import raw data
    # df = rotate_points(df, 180, 'A_base')  ## rotate points 180 deg to correct field error (line A only)
    df = shift_points(df,'C_base')           ## shift all points to align TS base with GPS base
    df = rotate_points(df,angle,'C_base')    ## rotate points arbitrary angle to correct for field misalignment.  iterate over this function
    df = calc_misfit(df)            ## calculate a chi-square misfit
    return df['misfit'].sum()       ## return the sum of misfits

def plot_angle(angle):
    df = import_data('/Users/jasondec/0_gradwork/0_hcf/TS_C_v0.csv','/Users/jasondec/0_gradwork/0_hcf/GPS_C_v0.csv')  ## import raw data
    # df = rotate_points(df, 180, 'A_base')  ## rotate points 180 deg to correct field error (line A only)
    df = shift_points(df,'C_base')           ## shift all points to align TS base with GPS base
    df = rotate_points(df,angle,'C_base')    ## rotate points arbitrary angle to correct for field misalignment.  iterate over this function
    df = calc_misfit(df)            ## calculate a chi-square misfit
    return df       ## return the sum of misfits

## calculate minimum result of single-variable function
min = optimize.minimize_scalar(optimize_rotation)
print min
    # plot it
df = plot_angle(min.x)
plt.scatter(df['x_working'], df['y_working'], color='orange')
    # save it
df.to_csv('/Users/jasondec/0_gradwork/0_hcf/TS_C_v1.csv')


## plot multiple angles
# for a in range(0,0):
#     df = plot_angle(a)
#     plt.scatter(df['x_working'], df['y_working'], color='blue')

# ## plot raw data, no rotation or shift
# plt.scatter(df['X0'], df['Y0'], color='blue')

## plot all GPS points, raw
# gps = pd.read_csv('/Users/jasondec/0_gradwork/0_hcf/raw_gps.csv', index_col='Name')
# plt.scatter(gps['Lon'], gps['Lat'], color='purple')

plt.show()
# print df
exit()
