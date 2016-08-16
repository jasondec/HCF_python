#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt

from HCF_functions import import_data, shift_points, rotate_points, calc_misfit_simple, wgs84_to_utm, dist_from_base, \
    init_plot, make_plot, optimize_rotation_weighted, change_var

## Total Station Line A
rootpath = '/Users/jasondec/0_gradwork/0_hcf/'
TS_data_file = rootpath+'TS_A_v0.csv'
GPS_data_file = rootpath+'GPS_A_v0.csv'
outfile = rootpath+'TS_A_v1.csv'

## Plot prep
init_plot()


## Import
data = import_data(TS_data_file,GPS_data_file)  ## import raw data

## XY points
plt.scatter(data['x_working'], data['y_working'], color='grey')
# rotate_points(data, 180, 'A_base')
shift_points(data,'A_base')
calc_misfit_simple(data)
# print data
# print data['misfit'].sum()
working = data.copy()

plt.scatter(data['x_working'], data['y_working'], color='blue')
plt.scatter(data['gps_lon'], data['gps_lat'], color='red')

## Stats
dist_from_base(data,'A_base')
data['dx_precision'] = 5e-6*data['basedist']+0.001

## Elevation
data['elev_diff'] = data['gps_elev'] - data['z_working']

## print all integer values
# list = range(-180,180,1)
# for a in list:
#     print str(a)+" "+str(optimize_rotation_weighted(a,data,'A_base'))
#     # plt.plot(a,optimize_rotation_weighted(a,data,'A_base'))


## calculate minimum result of single-variable function
print working['misfit'].sum()
# print optimize.minimize_scalar(optimize_rotation_weighted,bounds=(-180,180),args=(working,'A_base'))
# print optimize.fmin(optimize_rotation_weighted,10,args=(working,'A_base'),full_output=True)
# print optimize.minimize(optimize_rotation_weighted,-18,args=(working,'A_base'))
# print working['misfit'].sum()

# print df['misfit'].sum()

# df = plot_angle(180,df)
# plt.scatter(df['x_working'], df['y_working'], color='purple')

# df = plot_angle(220,df)
# plt.scatter(df['x_working'], df['y_working'], color='purple')

## export
data.to_csv(outfile)

## make plot
make_plot()
exit()
