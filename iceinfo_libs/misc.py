import sys
import numpy as np
from datetime import datetime as dt
from netCDF4 import num2date, Dataset

def epoch(d_in):
 """din is a datetime list."""
 return [ (x-dt(1970,1,1)).total_seconds() for x in d_in ]

def readNC(f_in,var=False,dims=False,longitude='longitude',latitude='latitude',time='time',fill_value=np.nan):
  """
  reads in netCDF file variables with optional dimension variables.

  Parameters:
  netCDF file in, variable name, dims=F or T, \
          longitude='lon name', lat='lat name', \
          time='time name', fill_value=np.nan.

  Returns:
  if var: var, if dims=True: dtime,lon,lat, if both: dims and var
  """
  if not var and not dims:
   raise Exception("not requesting anything. exiting.")
  if var:
   u = Dataset(f_in,'r').variables[var][:].filled(fill_value=fill_value)
  if dims:
   temp = Dataset(f_in,'r').variables[time][:].filled()
   units = Dataset(f_in,'r').variables[time].units
   calendar = Dataset(f_in,'r').variables[time].calendar
   dtime = num2date(temp,units=units,calendar=calendar,only_use_cftime_datetimes=False,only_use_python_datetimes=False)
   lon = Dataset(f_in,'r').variables[longitude][:].filled(fill_value=fill_value)
   lat = Dataset(f_in,'r').variables[latitude][:].filled(fill_value=fill_value)
   if var:
    return dtime,lon,lat,u
   else: return dtime,lon,lat
  else: return u
