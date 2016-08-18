#!/Users/jasondec/anaconda2/bin/python

def rotate_xy(xPoint,yPoint,x0,y0,angle):
	import math

	xDiff = xPoint - x0
	yDiff = yPoint - y0
	xNew = x0 + xDiff * math.cos(angle) - yDiff * math.sin(angle)
	yNew = y0 + yDiff * math.cos(angle) + xDiff * math.sin(angle)
	return xNew,yNew


def import_v0_data(TS_data_file,GPS_data_file):
	import pandas as pd
	import matplotlib.pyplot as plt

	TS_data = pd.read_csv(TS_data_file, comment='#', index_col='ID')  ## import CSV file using ID col as the indexer
	GPS_data = pd.read_csv(GPS_data_file, comment='#', index_col='gps_point')  ## import CSV file using Point col as indexer
	dataframe = pd.merge(TS_data, GPS_data, left_index=True, right_index=True, how='left')

	## copy original values to new working columns
	dataframe['x_working'] = dataframe['X0']
	dataframe['y_working'] = dataframe['Y0']
	dataframe['z_working'] = dataframe['Z0']

	## Plot raw points
	# plt.scatter(dataframe['x_working'], dataframe['y_working'], color='grey')
	# plt.scatter(dataframe['gps_lon'], dataframe['gps_lat'], color='red')

	return dataframe

def import_v1_data(file):
	import pandas as pd

	dataframe = pd.read_csv(file, comment='#', index_col='ID')  ## import CSV file using ID col as the indexer
	return dataframe

def shift_points(dataframe,base):
	## Shift all TS points by base - A_base_TS in x,y,z
	delX = dataframe.loc[base]['gps_lon'] - dataframe.loc[base]['x_working']
	delY = dataframe.loc[base]['gps_lat'] - dataframe.loc[base]['y_working']
	delZ = dataframe.loc[base]['gps_elev'] - dataframe.loc[base]['z_working']

	# delX = dataframe.loc[base]['x_working'] - dataframe.loc[base]['gps_lon']
	# delY = dataframe.loc[base]['y_working'] - dataframe.loc[base]['gps_lat']
	# delZ = dataframe.loc[base]['z_working'] - dataframe.loc[base]['gps_elev']

	dataframe['x_working'] = dataframe['x_working'] + delX
	dataframe['y_working'] = dataframe['y_working'] + delY
	dataframe['z_working'] = dataframe['z_working'] + delZ
	return dataframe


def rotate_points(dataframe,angle,base):
	import math
	from HCF_functions import rotate_xy

	xBase = dataframe.loc[base]['x_working']  # x-coord of base
	yBase = dataframe.loc[base]['y_working']  # y-coord of base

	dataframe['x_working'], dataframe['y_working'] = rotate_xy(dataframe['x_working'], dataframe['y_working'], xBase, yBase, angle * math.pi / 180)
	return dataframe


def calc_misfit_weighted(dataframe):
	import numpy as np

	## calculate chi-square for each point (chisqr X + chisqrY)
	dataframe['chi_sqr'] = np.square(dataframe['x_working'] - dataframe['gps_lon']) / np.square(dataframe['gps_lon']) + np.square(dataframe['y_working'] - dataframe['gps_lat']) / np.square(dataframe['gps_lat'])
	## weight misfit by inverse of gps accuracy
	dataframe['misfit'] = dataframe['chi_sqr'] / dataframe['gps_horiz_acc']
	return dataframe


def calc_misfit_simple(dataframe):
	import numpy as np

	## calculate misfit
	a = dataframe['x_working'] - dataframe['gps_lon']
	b = dataframe['y_working'] - dataframe['gps_lat']
	c = np.square(a) + np.square(b)
	dataframe['misfit'] = np.sqrt(c)

	return dataframe


def wgs84_to_utm(dataframe,xIn,yIn,xOut,yOut):
	import utm
	def getUTMs(row):
		import pandas as pd
		tup = utm.from_latlon(row.loc[yIn], row.loc[xIn])
		return pd.Series(tup[:2])
	dataframe[[xOut,yOut]] = dataframe[[yIn,xIn]].apply(getUTMs, axis=1)
	return dataframe


def dist_from_base(dataframe,base):
	import numpy as np

	xDist = dataframe['x_working'] - dataframe.loc[base]['x_working']
	yDist = dataframe['y_working'] - dataframe.loc[base]['y_working']
	dataframe['basedist'] = np.sqrt(np.square(xDist)+np.square(yDist))
	return dataframe


def init_plot():
	import matplotlib.pyplot as plt
	plt.figure(figsize=(8, 8), dpi=80)
	plt.grid(True)
	plt.axes().set_aspect('equal', 'datalim')


def optimize_rotate_simple(angle,df,base):
	import numpy as np
	import math
	from HCF_functions import rotate_xy
	import matplotlib.pyplot as plt

	sum = 0
	pick = np.isfinite(df['gps_lat'])
	x0 = df.loc[base]['x_working']
	y0 = df.loc[base]['y_working']
	for index, row in df[pick].iterrows():
		newX, newY = rotate_xy(row['x_working'],row['y_working'],x0,y0, angle * math.pi / 180)
		gpsX, gpsY = row['gps_lon'], row['gps_lat']
		a = newX - gpsX
		b = newY - gpsY
		c = np.square(a) + np.square(b)
		misfit = np.sqrt(c)
		sum = sum + misfit
		print angle, index, sum
	plt.scatter(df['x_working'], df['y_working'], color='orange')
	return sum

def optimize_rotate_weighted(angle,df,base):
	import numpy as np
	import math
	import utm
	from HCF_functions import rotate_xy
	import matplotlib.pyplot as plt

	sum = 0
	pick = np.isfinite(df['gps_lat'])
	k = utm.from_latlon(df.loc[base]['y_working'],df.loc[base]['x_working'])
	x0 = k[0]
	y0 = k[1]
	for index, row in df[pick].iterrows():
		i = utm.from_latlon(row['y_working'], row['x_working'])
		j = utm.from_latlon(row['gps_lat'], row['gps_lon'])
		gpsX, gpsY = j[0], j[1]
		newX, newY = rotate_xy(i[0],i[1],x0,y0, angle * math.pi / 180)

		a = newX - gpsX
		b = newY - gpsY
		c = np.square(a) + np.square(b)
		misfit = np.sqrt(c)
		misfit = np.sqrt(c) / row['gps_horiz_acc']
		sum = sum + misfit
		# print angle, index, misfit
	plt.scatter(df['x_working'], df['y_working'], color='orange')
	print angle, sum
	return sum

def fitline(df):
	import numpy as np
	line = np.polyfit(df['x_working'],df['y_working'],1)
	slope = line[0]
	intercept = line[1]
	# yfit = [intercept + slope * xi for xi in df['x_working']]
	# plt.plot(df['x_working'], yfit)
	return slope,intercept
