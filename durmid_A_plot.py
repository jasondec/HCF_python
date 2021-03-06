#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import HCF_functions as hcf
from shapely.geometry import Point, LineString

## Total Station Line C
rootpath = '/Users/jasondec/0_gradwork/0_classes/0_durmid/'
v1_file = rootpath+'durmid_A_v1.csv'
outfile = rootpath+'durmid_A_v2.csv'
base = 'BC_1'

## Import
data = hcf.import_v1_data(v1_file)  ## import rotated data


working = data.copy()
hcf.init_plot()
plt.scatter(data['x_working'], data['y_working'], color='black')
plt.scatter(data['gps_lon'], data['gps_lat'], color='red')

## best fit straight line of points
slope, intercept = hcf.fitline(data)

## define Shapely linestring using westmost and eastmost endpoints
point1 = Point(data['x_working'].min(),slope*data['x_working'].min()+intercept)
point2 = Point(data['x_working'].max(),slope*data['x_working'].max()+intercept)
ls = LineString([point1,point2])

## iterate through dataframe, project each TS point on Shapely line.  Determine position on line and absolute x,y value
for index,row in data.iterrows():
	pointN = Point(row['x_working'],row['y_working'])
	projectN = ls.project(pointN)
	data.set_value(index,'position_on_line',projectN)
	globalN = ls.interpolate(projectN)
	data.set_value(index,'x_project',globalN.x)
	data.set_value(index,'y_project',globalN.y)
	offsetN = globalN.distance(pointN)
	data.set_value(index, 'offset_from_line', offsetN)

data = data.sort_values(by='position_on_line',ascending='true')
print data

## plot points projected on best fit line
plt.scatter(data['x_project'], data['y_project'], color='pink')

## init Figure 2
plt.figure(num=2, figsize=(13, 3), dpi=80)
plt.grid(True)
# plt.axes().set_aspect('equal', 'datalim')
plt.axis([data['position_on_line'].min()-20,data['position_on_line'].max()+20,data['z_working'].min()-4,data['z_working'].max()+4])
plt.scatter(data['position_on_line'], data['z_working'], color='black')
plt.plot(data['position_on_line'], data['z_working'], color='black')

## convert to lat/lon
hcf.convert_working_to_latlon(data,11,'S')

## export
data.to_csv(outfile)

## make plot
plt.show()
exit()
