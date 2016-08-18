#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt
import numpy as np
import HCF_functions as hcf
import utm

## Total Station Line C
rootpath = '/Users/jasondec/0_gradwork/0_hcf/'
TS_data_file = rootpath+'TS_A_v0.csv'
GPS_data_file = rootpath+'GPS_A_v0.csv'
outfile = rootpath+'TS_A_v1.csv'
base = 'A_base'

## Plot prep
hcf.init_plot()


## Import
data = hcf.import_data(TS_data_file,GPS_data_file)  ## import raw data

## XY points
plt.scatter(data['x_working'], data['y_working'], color='grey')
hcf.shift_points(data,base)
# hcf.rotate_points(data, 180, base)
# hcf.calc_misfit_simple(data)
working = data.copy()

plt.scatter(data['x_working'], data['y_working'], color='black')
plt.scatter(data['gps_lon'], data['gps_lat'], color='red')

## Stats
hcf.dist_from_base(data,base)
data['dx_precision'] = 5e-6*data['basedist']+0.001

## Elevation
data['elev_diff'] = data['gps_elev'] - data['z_working']


## 165.23694478019937 degrees rotation, 7.810900286653812 total misfit
## calculate minimum result of function
min_angle = optimize.minimize_scalar(hcf.optimize_rotate_weighted,args=(working,base))
print min_angle

## apply optimized angle to dataframe
hcf.rotate_points(data, min_angle.x, base)

## draw rotated data
plt.scatter(data['x_working'], data['y_working'], color='blue')


## export
data.to_csv(outfile)

## make plot
hcf.make_plot()
exit()
