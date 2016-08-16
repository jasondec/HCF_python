#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt
import numpy as np

from HCF_functions import import_data, shift_points, rotate_points, calc_misfit_simple, dist_from_base, \
    init_plot, make_plot, optimize_rotate_simple

## Total Station Line A
rootpath = '/Users/jasondec/0_gradwork/0_hcf/'
TS_data_file = rootpath+'TS_E_v0.csv'
GPS_data_file = rootpath+'GPS_E_v0.csv'
outfile = rootpath+'TS_E_v1.csv'

## Plot prep
init_plot()


## Import
data = import_data(TS_data_file,GPS_data_file)  ## import raw data

## XY points
plt.scatter(data['x_working'], data['y_working'], color='grey')
# rotate_points(data, 180, 'E_base')
shift_points(data,'E_base')
calc_misfit_simple(data)
working = data.copy()

plt.scatter(data['x_working'], data['y_working'], color='black')
plt.scatter(data['gps_lon'], data['gps_lat'], color='red')

## Stats
dist_from_base(data,'E_base')
data['dx_precision'] = 5e-6*data['basedist']+0.001

## Elevation
data['elev_diff'] = data['gps_elev'] - data['z_working']


## calculate minimum result of function
min_angle = optimize.minimize_scalar(optimize_rotate_simple,args=(working,'E_base'))
## 165.23694478019937 degrees rotation, 7.810900286653812 total misfit
print min_angle ## print results

## apply optimized angle to dataframe
rotate_points(data, min_angle.x, 'E_base')
## draw rotated data
plt.scatter(data['x_working'], working['y_working'], color='blue')


## export
data.to_csv(outfile)

## make plot
make_plot()
exit()
