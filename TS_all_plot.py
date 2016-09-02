#!/Users/jasondec/anaconda2/bin/python

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import HCF_functions as hcf
from shapely.geometry import Point, LineString

## Total Station Line C
rootpath = '/Users/jasondec/0_gradwork/0_hcf/'
v1_file = rootpath + 'TS_all_v2.csv'
outfile = rootpath + 'TS_all_v3.csv'
# base = 'C_base'

## Import
data = hcf.import_v1_data(v1_file)  ## import rotated data

working = data.copy()
hcf.init_plot()
plt.scatter(data['x_working'], data['y_working'], color='black')
plt.scatter(data['gps_lon'], data['gps_lat'], color='red')


def fitline_plot(df):
	## best fit straight line of points
	slope, intercept = hcf.fitline(df)

	## define Shapely linestring using westmost and eastmost endpoints
	point1 = Point(df['x_working'].min(), slope * df['x_working'].min() + intercept)
	point2 = Point(df['x_working'].max(), slope * df['x_working'].max() + intercept)
	ls = LineString([point1, point2])

	## iterate through dfframe, project each TS point on Shapely line.  Determine position on line and absolute x,y value
	for index, row in df.iterrows():
		pointN = Point(row['x_working'], row['y_working'])
		projectN = ls.project(pointN)
		df.set_value(index, 'position_on_line', projectN)
		globalN = ls.interpolate(projectN)
		df.set_value(index, 'x_project', globalN.x)
		df.set_value(index, 'y_project', globalN.y)
		offsetN = globalN.distance(pointN)
		df.set_value(index, 'offset_from_line', offsetN)

	df = df.sort_values(by='position_on_line', ascending='true')
	print df

	## plot points projected on best fit line
	plt.scatter(df['x_project'], df['y_project'], color='pink')

	## init Figure 2
	plt.figure(num=2, figsize=(13, 3), dpi=80)
	plt.grid(True)
	# plt.axes().set_aspect('equal', 'dflim')
	plt.axis([df['position_on_line'].min() - 20, df['position_on_line'].max() + 20, df['z_working'].min() - 4,
	          df['z_working'].max() + 4])
	plt.scatter(df['position_on_line'], df['z_working'], color='black')
	plt.plot(df['position_on_line'], df['z_working'], color='black')


# fitline_plot(data1)
# fitline_plot(data2)

## export
# data.to_csv(outfile)

## make plot
plt.show()
exit()
