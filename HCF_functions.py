#!/Users/jasondec/anaconda2/bin/python

def rotate_xy(xPoint,yPoint,x0,y0,angle):
    import math

    xDiff = xPoint - x0
    yDiff = yPoint - y0
    xNew = x0 + xDiff * math.cos(angle) - xDiff * math.sin(angle)
    yNew = y0 + yDiff * math.cos(angle) + yDiff * math.sin(angle)
    return xNew,yNew

def import_data(TS_data_file,GPS_data_file):
    import pandas as pd
    import matplotlib.pyplot as plt

    TS_data = pd.read_csv(TS_data_file, comment='#', index_col='ID')  ## import CSV file using ID col as the indexer
    GPS_data = pd.read_csv(GPS_data_file, comment='#', index_col='gps_point')  ## import CSV file using Point col as indexer
    df = pd.merge(TS_data, GPS_data, left_index=True, right_index=True, how='left')

    ## copy original values to new working columns
    df['x_working'] = df['X0']
    df['y_working'] = df['Y0']
    df['z_working'] = df['Z0']

    ## Plot raw points
    # plt.scatter(df['x_working'], df['y_working'], color='grey')
    # plt.scatter(df['gps_lon'], df['gps_lat'], color='red')

    return df

def shift_points(df,base):
    ## Shift all TS points by base - A_base_TS in x,y,z
    delX = df.loc[base]['gps_lon'] - df.loc[base]['x_working']
    delY = df.loc[base]['gps_lat'] - df.loc[base]['y_working']
    delZ = df.loc[base]['gps_elev'] - df.loc[base]['z_working']

    df['x_working'] = df['x_working'] + delX
    df['y_working'] = df['y_working'] + delY
    df['z_working'] = df['z_working'] + delZ
    return df

def rotate_points(df,angle,base):
    import math
    from HCF_functions import rotate_xy

    xBase = df.loc[base]['x_working']  # x-coord of base
    yBase = df.loc[base]['y_working']  # y-coord of base

    df['x_working'], df['y_working'] = rotate_xy(df['x_working'], df['y_working'], xBase, yBase, angle * math.pi / 180)
    return df

def calc_misfit_weighted(df):
    import numpy as np

    ## calculate chi-square for each point (chisqr X + chisqrY)
    df['chi_sqr'] = np.square(df['x_working'] - df['gps_lon']) / np.square(df['gps_lon']) + np.square(df['y_working'] - df['gps_lat']) / np.square(df['gps_lat'])
    ## weight misfit by inverse of gps accuracy
    df['misfit'] = df['chi_sqr'] / df['gps_horiz_acc']
    return df

def calc_misfit(df):
    import numpy as np

    ## calculate misfit
    df['misfit'] = np.square(df['x_working'] - df['gps_lon']) / np.square(df['gps_lon']) + np.square(df['y_working'] - df['gps_lat']) / np.square(df['gps_lat'])
    return df

def wgs84_to_utm(df):
    import utm
    def getUTMs(row):
        import pandas as pd
        tup = utm.from_latlon(row.loc['y_working'], row.loc['x_working'])
        return pd.Series(tup[:2])
    df[['easting','northing']] = df[['y_working','x_working']].apply(getUTMs, axis=1)
    print df
    return df

def dist_from_base(df,base):
    import numpy as np

    xDist = df['x_working'] - df.loc[base]['x_working']
    yDist = df['y_working'] - df.loc[base]['y_working']
    df['basedist'] = np.sqrt(np.square(xDist)+np.square(yDist))
    return df

def plot_mult_angles(df,angles):
    for a in range(angles):
        df = plot_angle(a)
        plt.scatter(df['x_working'], df['y_working'], color='blue')