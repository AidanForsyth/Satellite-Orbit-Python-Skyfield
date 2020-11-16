'''
Aidan Forsyth 
Kepler Communications 
Challenge Question 3
'''

from skyfield.api import Topos, load

stations_url = 'http://celestrak.com/NORAD/elements/stations.txt' #paste whatever TLE text file data from Celestrak
satellites = load.tle_file(stations_url)

by_name = {sat.name: sat for sat in satellites} #creating a dictionary that includes all stations in station.txt
satellite = by_name['ISS (ZARYA)'] #able to call a station of choice by name (could also call by catalog #)
print(satellite) #displays satellite name

Latitude = []
Longitude = []

for i in range(0, 3840): #cycles through a given time range (24-hr)
    ts = load.timescale()
    t = ts.utc(2020, 1, 1, i/160, 0, 0) #splits up the time step to be every 22.5 seconds
    geocentric = satellite.at(t)
    subpoint = geocentric.subpoint()
    
    Lat = subpoint.latitude #gets the latitude 
    Long = subpoint.longitude #gets the longtitude 

    
    Latitude.append(Lat.degrees) #pulls the lat in degrees and adds it to a list Latitude 
    Longitude.append(Long.degrees) #pulls the lat in degrees and adds it to a list Longitude
    
    #print('-----', t.utc_strftime('On %Y %b %d %H:%M:%S'), '-----')
    
import os
os.environ['PROJ_LIB'] = 'C:/Users/aidan/Anaconda3/Lib/site-packages/mpl_toolkits/basemap'
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from itertools import chain

def draw_map(m, scale=0.5):
    #draw a shaded-relief image
    m.shadedrelief(scale=scale)
    
    #lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(-90, 90, 11), labels=[1,1,0,0])
    lons = m.drawmeridians(np.linspace(-180, 180, 11), labels=[0,0,0,1])

    #keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)
    
    #cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='--', alpha=0.7, color='gray')
        
fig = plt.figure(figsize=(10, 10))


m = Basemap(projection='cyl', resolution=None,
            llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180, )

for i in range(0, 3840, 240):
    m.scatter(Longitude[i:i+240], Latitude[i:i+240], latlon=True, marker='.') #plots the points ever orbit (1 orbit = 240 data points)



plt.title('24-hr Satellite Orbit', loc='center')
plt.ylabel('Latitude', labelpad = 40)
plt.xlabel('Longitude', labelpad = 30)
draw_map(m)
plt.savefig('KeplerQ3.png')
plt.show()