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
from dateutil.parser import parse
from datetime import datetime as dt

import matplotlib.cm as mplcm
import cmocean.tools as cmtools

from misc.dates import EpochConverter as ec
from misc.misc import nearest,polymask
from scipy.interpolate import interp1d

from dataIO.readdata import readBuoyTrack,readNC
from dataIO.importAMSR2 import importAMSR2 as iA
from dataProcessing.dataprocessing import pol2orthg

from plotLib.maplib import plotmercator,plotpolarstereo
from plotLib.plotterdataclass import xydata,cntrdata,grddata,vecdata
from dataIO.readdata import readCsv

plot_iceinfo = "/home/takka/symlinks/myDesktop/ice-info/new/ecmwf/figure"
ECMWFDir = '/home/takka/symlinks/myDesktop/ice-info/ecmwf/nc'
ver="ver20240201"
# day = '20220208'

def importTrack():
 trackf = f"/home/takka/symlinks/myDesktop/ice-info/planned_track_{ver}.csv"
 data = readCsv(trackf)
 lon = [ float(x) for x in data["lon"] ]
 lat = [ float(x) for x in data["lat"] ]
 return lon,lat,data

def importECMWF(day,zhr):
 nc_in=f"{ECMWFDir}/{day}-{zhr}-wave.nc"
 #
 dtime,lons,lats,h = readNC(nc_in,'swh',dims=True)
 t = readNC(nc_in,'pp1d')
 d = readNC(nc_in,'mwd')
 u,v = pol2orthg(t,d)
 x,y = np.meshgrid(lons,lats) #,indexing='ij')
 return dtime,x,y,h,u,v

def main(day,zhr):
 out_dir = f"{plot_iceinfo}/{day[:4]}/{day[4:6]}/{day[6:8]}/{zhr}Z"
 if not os.path.isdir(out_dir): os.makedirs(out_dir)
 #cmap = mplcm.rainbow
 cmap = mplcm.turbo
 ms = 18
 vlim = (0,10)
 #if parse(day)>dt(2022,8,7):
 # vlim=(0,5);tvec=10;vlegx=0.78;vlegy=0.885;ms=18
 # plt_extent = [-17.0,30.5,71.0,82.4];rgs=20
 #else:
 # vlim=(0,2.5);tvec=8;vlegx=0.78;vlegy=0.900;ms=14
 # plt_extent = [-10.0,25.5,73.0,82.4];rgs=18
 #
 lon,lat,track = importTrack()
 trcks = [xydata(x=lon,y=lat,lab="Planned track",color="brown")]
 # clon = 0;clat = 80; # lgloc='lower right'; lgcol=4;
 alpha = 0.8
 #
 # plt_extent = [-10,20,-70.0,-60]
 plt_extent = [-45,55,-70.0,-30]
 lat_tiks = np.arange(-30,-89.,-10)
 lon_tiks = np.arange(-90,180,10)
 # x,y,sic = iA(day,hem='S')
 # sic = np.where( ((x%360)<0.25),np.nan,sic)
 ### assign contour
 # cntr = [cntrdata(x=x%360,y=y,z=sic,cntrs=[0.15,0.8],lstyle=['--','-'],color='0.2',lw=2)]
 # do plot #,
 dtime,xw,yw,h,u,v = importECMWF(day,zhr)
 iint = 1
 dtimeS = [ parse(x) for x in track["date"] ] 
 lonfield = interp1d(ec(dtimeS,"date2num"),lon)
 latfield = interp1d(ec(dtimeS,"date2num"),lat)
 for ii,dd in enumerate(dtime[::iint]):
  pts = []
  for i1,st in enumerate(track["station"]):
   if st=="":
    lab=None
   else: lab=st
   clr = track["color"][i1] 
   pts += [xydata(x=lon[i1],y=lat[i1],lab=lab,alpha=1,mfc=clr,mec=clr,style=track["marker"][i1],ms=18)]
  cntr = []
  i0 = ii*iint
  print("\n plotting {}".format(str(dd)))
  # fout = os.path.join(out_dir,dd.strftime('%Y%m%d%H%M_wave'))
  fout = os.path.join(out_dir,f"{dd:%Y%m%d%H%M}-{zhr}-wave")
  title =f"{day} {zhr}Z ECMWF Opendata wave for &\nXXXX SIC at {dd: UTC %H:%M %d %b %Y}\nPlanned track {ver}."
  ### get buoy data
  # pts += [xydata(x=lonfield(ec(dd,"date2num")),y=latfield(ec(dd,"date2num")),lab="Shirase loc",alpha=0.9,mec="0.9",style="$WQ$")]
  grd = grddata(x=xw,y=yw,z=h[i0,:,:],cmap=cmap,vlim=vlim,\
   lab='Significant wave height (m)')
  vec = vecdata(x=xw,y=yw,u=u[i0,:,:],v=v[i0,:,:],\
    # lab=(0.75,0.860,10,f'10 s $T_{{p}}$ period\nwave vector'),\
    lab=(0.75,0.84,10,f'10 s $T_{{p}}$ period\nwave vector'),\
    scale=None,width=5e-4,regrid_shape=18,color='k')
  ### plot
  #inset=dict(extent=[-1.0,1.0,-69.7,-68.3],central_lon=38.5)
  _ = plotmercator(cntr=cntr,pts=pts,vec=vec,grd=grd,trcks=trcks,\
    central_longitude=70,plt_extent=plt_extent,\
    fout=fout,lat_tiks = lat_tiks,lon_tiks = lon_tiks,fontsize=20,\
    cbarextend='max',title=title,inset=False,coastison=True,\
    legloc='lower right',legend=3,scalebar=dict(len=500,loc=(0.25,0.05)))
  # _ = plotpolarstereo(cntr=cntr,pts=pts,vec=vec,grd=grd,trcks=trcks,\
  #   central_longitude=30,central_latitude=-78.5,plt_extent=plt_extent,\
  #   fout=fout,lat_tiks = lat_tiks,lon_tiks = lon_tiks,fontsize=20,\
  #   cbarextend='max',title=title,inset=False,coastison=True,\
  #   legloc='upper center',legend=7) 

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
 \033[1;35ma Python script to do blah.

 The argument 'arg' is a blah.\033[1;0m

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
