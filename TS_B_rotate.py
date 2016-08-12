#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt

from HCF_functions import import_data, shift_points, rotate_points, calc_misfit_weighted, wgs84_to_utm

## Total Station Line A
rootpath = '/Users/jasondec/0_gradwork/0_hcf/'
TS_data_file = rootpath+'TS_C_v0.csv'
GPS_data_file = rootpath+'GPS_C_v0.csv'
outfile = rootpath+'TS_C_v1.csv'


def optimize_rotation(angle):
    df = import_data('/Users/jasondec/0_gradwork/0_hcf/TS_B_v0.csv','/Users/jasondec/0_gradwork/0_hcf/GPS_B_v0.csv')  ## import raw data
    df = shift_points(df,'B_base')           ## shift all points to align TS base with GPS base
    df = rotate_points(df,angle,'B_base')    ## rotate points arbitrary angle to correct for field misalignment.  iterate over this function
    df = calc_misfit_weighted(df)            ## calculate a chi-square misfit
    return df['misfit'].sum()       ## return the sum of misfits

def plot_angle(angle):
    df = import_data('/Users/jasondec/0_gradwork/0_hcf/TS_B_v0.csv','/Users/jasondec/0_gradwork/0_hcf/GPS_B_v0.csv')  ## import raw data
    df = shift_points(df,'B_base')           ## shift all points to align TS base with GPS base
    df = rotate_points(df,angle,'B_base')    ## rotate points arbitrary angle to correct for field misalignment.  iterate over this function
    df = calc_misfit_weighted(df)            ## calculate a chi-square misfit
    return df       ## return the sum of misfits

## calculate minimum result of single-variable function
min = optimize.minimize_scalar(optimize_rotation)
print min
    # plot it
df = plot_angle(min.x)
plt.scatter(df['x_working'], df['y_working'], color='orange')
    # save it
df.to_csv('/Users/jasondec/0_gradwork/0_hcf/TS_B_v1.csv')


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
