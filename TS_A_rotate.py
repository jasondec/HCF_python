#!/Users/jasondec/anaconda2/bin/python

from scipy import optimize
import matplotlib.pyplot as plt

## Total Station Line A
TS_data_file = '/Users/jasondec/0_gradwork/0_hcf/TS_A_v0.csv'
GPS_data_file = '/Users/jasondec/0_gradwork/0_hcf/GPS_A_v0.csv'

def import_data(TS_data_file,GPS_data_file):
    import pandas as pd
    import matplotlib.pyplot as plt

    TS_data = pd.read_csv(TS_data_file, index_col='ID')  ## import CSV file using ID col as the indexer
    GPS_data = pd.read_csv(GPS_data_file, index_col='gps_point')  ## import CSV file using Point col as indexer
    df = pd.merge(TS_data, GPS_data, left_index=True, right_index=True, how='left')

    ## copy original values to new working columns
    df['x_working'] = df['X0']
    df['y_working'] = df['Y0']
    df['z_working'] = df['Z0']

    ## Plot raw points
    plt.scatter(df['x_working'], df['y_working'], color='grey')
    plt.scatter(df['gps_lon'], df['gps_lat'], color='red')

    return df

def shift_points(df):
    ## Shift all TS points by A_base_GPS - A_base_TS in x,y,z
    delX = df.loc['A_base']['gps_lon'] - df.loc['A_base']['X0']
    delY = df.loc['A_base']['gps_lat'] - df.loc['A_base']['Y0']
    delZ = df.loc['A_base']['gps_elev'] - df.loc['A_base']['Z0']

    df['x_working'] = df['x_working'] + delX
    df['y_working'] = df['y_working'] + delY
    df['z_working'] = df['z_working'] + delZ
    return df

def rotate_points(df,angle):
    import math
    from HCF_functions import rotate_xy

    xBase = df.loc['A_base']['x_working']  # x-coord of baseA
    yBase = df.loc['A_base']['y_working']  # y-coord of baseA

    df['x_working'], df['y_working'] = rotate_xy(df['x_working'], df['y_working'], xBase, yBase, angle * math.pi / 180)  ## rotate using external fcn
    return df


def calc_misfit(df):
    import numpy as np

    ## calculate chi-square for each point (chisqr X + chisqrY)
    df['chi_sqr'] = np.square(df['x_working'] - df['gps_lon']) / df['gps_lon'] + np.square(df['y_working'] - df['gps_lat']) / df['gps_lat']
    ## weight misfit by inverse of gps accuracy
    df['misfit'] = df['chi_sqr'] / df['gps_horiz_acc']
    return df


def optimize_rotation(angle):
    df = import_data('/Users/jasondec/0_gradwork/0_hcf/TS_A_v0.csv','/Users/jasondec/0_gradwork/0_hcf/GPS_A_v0.csv')  ## import raw data
    df = shift_points(df)           ## shift all points to align TS base with GPS base
    df = rotate_points(df,180)      ## rotate points 180 deg to correct field error (line A only)
    df = rotate_points(df,angle)    ## rotate points arbitrary angle to correct for field misalignment.  iterate over this function
    df = calc_misfit(df)            ## calculate a chi-square misfit
    return df['misfit'].sum()       ## return the sum of misfits


def plot_angle(angle):
    df = import_data('/Users/jasondec/0_gradwork/0_hcf/TS_A_v0.csv','/Users/jasondec/0_gradwork/0_hcf/GPS_A_v0.csv')  ## import raw data
    df = shift_points(df)           ## shift all points to align TS base with GPS base
    df = rotate_points(df,180)      ## rotate points 180 deg to correct field error (line A only)
    df = rotate_points(df,angle)    ## rotate points arbitrary angle to correct for field misalignment.  iterate over this function
    df = calc_misfit(df)            ## calculate a chi-square misfit
    return df       ## return the sum of misfits

## calculate minimum result of single-variable function
min = optimize.minimize_scalar(optimize_rotation)
print min

## rainbow plot
for a in range(-11,-1):
    df = plot_angle(a)
    plt.scatter(df['x_working'], df['y_working'], color='blue')

df = plot_angle(min.x)
plt.scatter(df['x_working'], df['y_working'], color='orange')


plt.show()
# print df
exit()
