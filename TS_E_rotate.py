#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt
import numpy as np
import HCF_functions as hcf
from shapely.geometry import Point, LineString

## Total Station Line A
rootpath = '/Users/jasondec/0_gradwork/0_hcf/'
TS_data_file = rootpath+'TS_E_v0.csv'
GPS_data_file = rootpath+'GPS_E_v0.csv'
outfile = rootpath+'TS_E_v1.csv'
base = 'E_base'

## Plot prep
hcf.init_plot()

## Import
data = hcf.import_v0_data(TS_data_file,GPS_data_file)  ## import raw data

## XY points
plt.scatter(data['x_working'], data['y_working'], color='grey')
# rotate_points(data, 180, base)
hcf.shift_points(data,base)
hcf.calc_misfit_simple(data)
working = data.copy()

plt.scatter(data['x_working'], data['y_working'], color='black')
plt.scatter(data['gps_lon'], data['gps_lat'], color='red')

## Stats
hcf.dist_from_base(data,base)
data['dx_precision'] = 5e-6*data['basedist']+0.001

## Elevation
data['elev_diff'] = data['gps_elev'] - data['z_working']


## calculate minimum result of function
min_angle = optimize.minimize_scalar(hcf.optimize_rotate_simple,args=(working,base))
## 165.23694478019937 degrees rotation, 7.810900286653812 total misfit
print min_angle ## print results

## apply optimized angle to dataframe
hcf.rotate_points(data, min_angle.x, base)
## draw rotated data
plt.scatter(data['x_working'], data['y_working'], color='blue')

## export
data.to_csv(outfile)

## make plot
plt.show()
exit()
