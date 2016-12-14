# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import fiona
from itertools import chain
import numpy as np


def draw_screen_poly( lats, lons, m):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, facecolor='red', alpha=0.4 )
    plt.gca().add_patch(poly)

lats = [28.473989, 28.5454, 28.453867, 28.487931]
lons = [76.957865, 77.1295, 76.999564, 76.971538]

shp = fiona.open('/home/delhivery/Documents/vsingh/Python_script/IADHS2006.shp')

#we can access the boundaries (the 2 lat,long pairs) using shp.bounds
bds = shp.bounds

#close the shp file
shp.close()

#define a variable called extra which we will use for padding the map when we display it (in this case I've selected a 10% pad)
extra = 0.1

#define the lower left hand boundary (longitude, latitude)
ll = (bds[0], bds[1])

#define the upper right hand boundary (longitude, latitude)
ur = (bds[2], bds[3])

#concatenate the lower left and upper right into a variable called coordinates
coords = list(chain(ll, ur))

#define variables for the width and the height of the map
w, h = coords[2] - coords[0], coords[3] - coords[1]

map = Basemap(
    #set projection to 'tmerc' which is apparently less distorting when close-in
    projection='tmerc',

    #set longitude as average of lower, upper longitude bounds
    lon_0 = np.average([bds[0],bds[2]]),

    #set latitude as average of lower,upper latitude bounds
    lat_0 = np.average([bds[1],bds[3]]),

    #string describing ellipsoid (‘GRS80’ or ‘WGS84’, for example). Not sure what this does...
    ellps = 'WGS84',
    
    #set the map boundaries. Note that we use the extra variable to provide a 10% buffer around the map
    llcrnrlon=coords[0] - extra * w,
    llcrnrlat=coords[1] - extra + 0.01 * h,
    urcrnrlon=coords[2] + extra * w,
    urcrnrlat=coords[3] + extra + 0.01 * h,

    #provide latitude of 'true scale.' Not sure what this means, I would check the Basemap API if you are a GIS guru
    lat_ts=0,

    #resolution of boundary database to use. Can be c (crude), l (low), i (intermediate), h (high), f (full) or None.
    resolution='i',
    
    #don't show the axis ticks automatically
    suppress_ticks=True)
# create the map

# load the shapefile, use the name 'states'
map.readshapefile('/home/delhivery/Documents/vsingh/Python_script/IADHS2006', name='states', drawbounds=True)

# collect the state names from the shapefile attributes so we can
# look up the shape obect for a state by it's name
state_names = []
for shape_dict in map.states_info:
    state_names.append(shape_dict['DHSREGEN'])

ax1 = plt.gca() # get current axes instance
ax2 = plt.gca()
# get Texas and draw the filled polygon
seg = map.states[state_names.index('Delhi')]
poly = Polygon(seg, facecolor='grey',edgecolor='blue')
ax1.add_patch(poly)

seg1 = map.states[state_names.index('Haryana')]
poly1 = Polygon(seg1, facecolor='grey',edgecolor='blue')
ax2.add_patch(poly1)

map.drawstates()
map.drawcoastlines()
map.drawstates()
map.drawmapboundary()
draw_screen_poly( lats, lons, map )

plt.show()
