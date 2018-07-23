#!/usr/bin/env python

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.util import add_cyclic_point
import matplotlib as mpl
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy.io.netcdf import netcdf_file

from windspharm.standard import VectorWind
from windspharm.tools import prep_data, recover_data, order_latdim
from windspharm.examples import example_data_path

mpl.rcParams['mathtext.default'] = 'regular'

ncu = Dataset('uv.nc', 'r')
u = ncu.variables['u'][:][:]
v = ncu.variables['v'][:][:]
times = ncu.variables['time'][:]
lons = ncu.variables['longitude'][:]
lats = ncu.variables['latitude'][:]
ncu.close()

u.shape
# print('ushape: ' + u.shape)
uwnd = u[:, 1, :, :]
vwnd = v[:, 1, :, :]

# The standard interface requires that latitude and longitude be the leading
# dimensions of the input wind components, and that wind components must be
# either 2D or 3D arrays. The data read in is 3D and has latitude and
# longitude as the last dimensions. The bundled tools can make the process of
# re-shaping the data a lot easier to manage.
uwnd, uwnd_info = prep_data(uwnd, 'tyx')
vwnd, vwnd_info = prep_data(vwnd, 'tyx')

# It is also required that the latitude dimension is north-to-south. Again the
# bundled tools make this easy.
lats, uwnd, vwnd = order_latdim(lats, uwnd, vwnd)

# Create a VectorWind instance to handle the computation of streamfunction and
# velocity potential.
w = VectorWind(uwnd, vwnd)

# Compute the streamfunction and velocity potential. Also use the bundled
# tools to re-shape the outputs to the 4D shape of the wind components as they
# were read off files.
sf_arr, vp_arr = w.sfvp()
sf_arr = recover_data(sf_arr, uwnd_info)
vp_arr = recover_data(vp_arr, uwnd_info)
# print(vp_arr.dtype.name)
# time.dtype
# lons.dtype
# lats.dtype
# exit()
# write output
filename = netcdf_file('./tmp_netcdf.nc', 'w')

# Dimensions
filename.createDimension('time', len(times))
filename.createDimension('lat', len(lats))
filename.createDimension('lon', len(lons))

sf = filename.createVariable('sf', 'f4', (
    'time',
    'lat',
    'lon',
))

vp = filename.createVariable('vp', 'f4', (
    'time',
    'lat',
    'lon',
))

lat = filename.createVariable('lat', 'f4', ('lat', ))
lon = filename.createVariable('lon', 'f4', ('lon', ))
time = filename.createVariable('time', 'i', ('time', ))

time[:] = times
lat[:] = lats
lon[:] = lons
sf[:, :, :] = sf_arr[:, :, :]
vp[:, :, :] = vp_arr[:, :, :]

filename.close()
