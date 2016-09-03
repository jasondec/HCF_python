#!/Users/jasondec/anaconda2/bin/python

import HCF_functions as hcf
import csv
import simplekml

kml = simplekml.Kml()

## AB
rootpath = '/Users/jasondec/0_gradwork/0_hcf/'
infile= rootpath+'profile_AB_v0.csv'
outfile = rootpath+'profile_AB_v1.csv'
kmlout = rootpath+'profile_AB_v1.kml'

filein= csv.reader(open(infile,'rU'))
for row in filein:
	if row[4] == 'x':
		pt = kml.newpoint(name=row[0], coords=[(row[1], row[2])])
		pt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
		pt.style.iconstyle.scale = 1
		pt.style.iconstyle.color = simplekml.Color.red
	else:
		pt = kml.newpoint(name=row[0], coords=[(row[1],row[2])])
		pt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
		pt.style.iconstyle.scale = .5
		pt.style.iconstyle.color = simplekml.Color.blue

kml.save(kmlout)