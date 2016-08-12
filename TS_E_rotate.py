#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt

from HCF_functions import import_data, shift_points, rotate_points, calc_misfit_weighted, wgs84_to_utm, dist_from_base

## Total Station Line A
rootpath = '/Users/jasondec/0_gradwork/0_hcf/'
TS_data_file = rootpath+'TS_C_v0.csv'
GPS_data_file = rootpath+'GPS_C_v0.csv'
outfile = rootpath+'TS_C_v1.csv'

## Import
df = import_data(TS_data_file,GPS_data_file)  ## import raw data

## XY points
plt.scatter(df['x_working'], df['y_working'], color='grey')
df = rotate_points(df, 180, 'E_base')  ## rotate points 180 deg to correct field error (line A only)
df = shift_points(df,'E_base')           ## shift all points to align TS base with GPS base
df = calc_misfit(df)            ## calculate a misfit of TS to GPS points

plt.scatter(df['x_working'], df['y_working'], color='blue')
plt.scatter(df['gps_lon'], df['gps_lat'], color='red')

## Stats
dist_from_base(df,'E_base')
df['dx_precision'] = 5e-6*df['basedist']+0.001

## Elevation
df['elev_diff'] = df['gps_elev'] - df['z_working']


def optimize_rotation(angle):
    df = rotate_points(df,angle,'E_base')    ## rotate points
    df = calc_misfit(df)            ## calculate a chi-square misfit
    plt.scatter(df['x_working'], df['y_working'], color='orange')
    return df['misfit'].sum()       ## return the sum of misfits

def plot_angle(angle):
    df = rotate_points(df,angle,'E_base')    ## rotate points
    df = calc_misfit(df)            ## calculate a misfit
    return df       ## return the sum of misfits


## calculate minimum result of single-variable function
min = optimize.minimize_scalar(optimize_rotation)
print min
#     plot it
df = plot_angle(min.x)
plt.scatter(df['x_working'], df['y_working'], color='orange')



## export
df.to_csv(outfile)


plt.show()
exit()
