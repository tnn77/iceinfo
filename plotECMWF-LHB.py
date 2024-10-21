#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on # Y/m/d

@author:
Notes:
"""

import sys,os
import timeit
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from dateutil.parser import parse

import matplotlib.cm as mplcm

### local libraries
from iceinfo_libs.misc import epoch,readNC
from iceinfo_libs.plotterdataclass import xydata,cntrdata,grddata,vecdata
from iceinfo_libs.maplib import plotmercator,plotpolarstereo

### set gloabl paths and functions
plot_iceinfo = "./test_fig"
ECMWFDir = './sample_files'
ver="ver20231201"

def importTrack():
 """digitised cruise plan obtained from JMSDF"""
 trackf = f"./sample_files/planned_track_{ver}.csv"
 df = pd.read_csv(trackf)
 lon = [ float(x) for x in df["lon"] ]
 lat = [ float(x) for x in df["lat"] ]
 return lon,lat,df

def importECMWF(day,zhr):
 nc_in=f"{ECMWFDir}/{day}-{zhr}-sfc.nc"
 #
 dtime,lons,lats,h = readNC(nc_in,'msl',dims=True)
 u = readNC(nc_in,'u10')
 v = readNC(nc_in,'v10')
 x,y = np.meshgrid(lons,lats) 
 return dtime,x,y,h,u,v

def main(day,zhr):
 ### set/create figure output directories
 out_dir = f"{plot_iceinfo}/{day[:4]}/{day[4:6]}/{day[6:8]}/{zhr}Z"
 if not os.path.isdir(out_dir): os.makedirs(out_dir)
 ### set figure layouts
 plt_extent = [-45,55,-70.0,-30]
 lat_tiks = np.arange(-30,-89.,-10)
 lon_tiks = np.arange(-90,180,10)
 # get plot data #,
 lon,lat,track = importTrack()
 trcks = [xydata(x=lon,y=lat,lab="Planned track",color="brown")]
 # 
 dtime,xw,yw,h,u,v = importECMWF(day,zhr)
 h = 1e-2*h
 dtimeS = [ parse(x) for x in track["date"] ] 
 ### if current Shirase pos is interpolated and shown (only somewhat useful inbound and outbound).
 lonfield = interp1d(epoch(dtimeS),lon)
 latfield = interp1d(epoch(dtimeS),lat)
 ### set the mslp contour values (make it a big range, so it will complain when it can't create a contour line)
 cntrs = [ x for x in range(950,1101,5) ]
 ### loop through lead times using the iint intervals
 iint = 1 # change figure output intervals
 for ii,dd in enumerate(dtime[::iint]):
  ### collates waypoints to show on the figure.
  pts = []
  for i1,st in enumerate(track["station"]):
   ### only include notable waypoints in the legends
   if isinstance(st,float):
    if np.isnan(st):
     lab=None
   else: lab=st
   clr = track["color"][i1] 
   pts += [xydata(x=lon[i1],y=lat[i1],lab=lab,alpha=1,mfc=clr,mec=clr,style=track["marker"][i1],ms=track["ms"][i1])]
  ### correct the ECMWF array index with intervals
  i0 = ii*iint
  print("\n plotting {}".format(str(dd)))
  ### set file name and title
  fout = os.path.join(out_dir,f"{dd:%Y%m%d%H%M}-{zhr}-sfc")
  title =f"{day} {zhr}Z ECMWF Opendata atmosphere &\nat {dd: UTC %H:%M %d %b %Y}\nPlanned track {ver}."
  ### get data
  # interpolated Shirase location
  pts += [xydata(x=lonfield(epoch([dd])),y=latfield(epoch([dd])),lab="Shirase loc",alpha=0.9,mec="0.9",style="$WQ$")]
  # wind vectors, there is a way to scale vector lengths automatically, which might be better if the coverage is changed often
  vec = vecdata(x=xw,y=yw,u=u[i0,:,:],v=v[i0,:,:],\
    lab=(0.75,0.850,10,'10 ms$^{-1}$\nwind vector'),\
    scale=None,width=5e-4,regrid_shape=20,color='red')
  # mslp contours
  cntr = []
  cntr += [ cntrdata(x=xw,y=yw,z=h[i0,:,:],cntrs=cntrs,\
    lstyle=[ '-' for x in range(1,100)], color='yellow', lw=2,\
    labformat='%d hPa') ]
  #
  ### do plot
  _ = plotmercator(cntr=cntr,pts=pts,vec=vec,trcks=trcks,\
    central_longitude=70,plt_extent=plt_extent,\
    fout=fout,lat_tiks = lat_tiks,lon_tiks = lon_tiks,fontsize=20,\
    title=title,coastison=True,\
    legloc='lower right',legend=3,scalebar=dict(len=500,loc=(0.25,0.05))) 
  # _ = plotpolarstereo(cntr=cntr,pts=pts,vec=vec,grd=grd,trcks=trcks,\
  #   central_longitude=30,central_latitude=-78.5,plt_extent=plt_extent,\
  #   fout=fout,lat_tiks = lat_tiks,lon_tiks = lon_tiks,fontsize=20,\
  #   cbarextend='max',title=title,coastison=True,inset=False,\
  #   legloc='upper center',legend=7,scalebar=dict(len=500)) 

@click.command(
cls=HelpColorsGroup,
help_headers_color='yellow',
help_options_color='green'
)
def cli():
 pass

@cli.command(context_settings=dict(help_option_names=["-h", "--help"],show_default=True))
### note on the usage. flags can be used in multiples like -pvh where as option inputs follows the option flag 
@click.argument('day')
@click.argument('zhr')
@click.option('--verbose','-v',is_flag=True,help='verbosity flag.')
### note that this repeat def cli() was by accident, but it makes it easier to use when only having a single command.
def cli(day,zhr,verbose):
 """
 \033[1;35ma Python script to do weather plots on Shirase.

 The arguments 'day' in YYYYmmdd, and zulu time 'zhr' 00 or 12.\033[1;0m

 """
 start = timeit.default_timer()
 sys.stdout.write("\n\033[1;33mExecuting {}\n\033[1;0m".format(os.path.basename(sys.argv[0])))

 main(day,zhr)

 stop = timeit.default_timer()
 mins, secs = divmod(stop-start, 60)
 hours, mins = divmod(mins, 60)
 sys.stdout.write("\n\033[1;33mPython script running time: %d:%d:%f.\n\033[1;0m" % (hours, mins, secs))

if __name__ == '__main__':
  cli()
