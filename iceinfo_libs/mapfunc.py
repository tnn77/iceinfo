"""
Created on # Y/m/d

@author:
Notes: functions to be used from maplib.py
"""

import numpy as np
import matplotlib as mpl
# mpl.use('svg')
# mpl.use('pdf')
mpl.use('agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def transformvec(vec):
 """
 incorrect direction of arrows in quiver, scale by cosine of latitude.
 see https://github.com/SciTools/cartopy/issues/1179
 """
 u_src_crs = vec.u / np.cos(vec.y/180*np.pi)
 v_src_crs = vec.v
 magnitude = np.sqrt(vec.u**2 + vec.v**2)
 magn_src_crs = np.sqrt(u_src_crs**2 + v_src_crs**2)
 uu = u_src_crs * magnitude / magn_src_crs
 vv = v_src_crs * magnitude / magn_src_crs
 return uu,vv

def plotvector(ax,vec,verbose,fontsize):
 # # # linewidths and edegecolors can be used to make the vector thicker.
 vecargs = dict(color=vec.color,scale_units=vec.scale_units,\
    scale=vec.scale, width=vec.width,headwidth=vec.headwidth,\
    headlength=vec.headlength,regrid_shape=vec.regrid_shape,pivot=vec.pivot,\
    linewidths=vec.lw,edgecolors=vec.ec
    )
 if verbose: print('vector now')
 uu,vv = transformvec(vec)
 qf = ax.quiver(vec.x,vec.y,uu,vv,transform=ccrs.PlateCarree(),\
 zorder=vec.zorder,**vecargs) #,pivot='mid',
 qk = ax.quiverkey(qf,*vec.lab,labelpos=vec.labpos,coordinates=vec.labcoord,\
  fontproperties={'size': int(fontsize*0.6)})
  
def plotcontour(ax,cntr,verbose,fontsize):
 if verbose: print('contours now')
 for citem in cntr:
  for icntr,vcntr in enumerate(citem.cntrs):
   ct = ax.contour(citem.x,citem.y,citem.z,[vcntr],zorder=citem.zorder,\
    linestyles=citem.lstyle[icntr],alpha=citem.alpha,\
    linewidths=citem.lw,colors=citem.color,transform=ccrs.PlateCarree())
   _ = plt.clabel(ct,colors=citem.color,fontsize=int(fontsize*0.75),inline=1,fmt=citem.labformat)

def plottracks(ax,trcks,verbose,fontsize):
 if verbose: print('tracks now')
 for trck in trcks:
  _ = ax.plot(trck.x,trck.y,color=trck.color,alpha=trck.alpha,\
  ls=trck.ls,lw=trck.lw,zorder=trck.zorder,\
  transform=ccrs.PlateCarree(),label=trck.lab)
#
def plotpoints(ax,pts,verbose,fontsize):
 if verbose: print('points now')
 for pt in pts:
  _ = ax.plot(pt.x,pt.y,marker=pt.style,color=pt.color,\
  mfc=pt.mfc,mec=pt.mec,mew=pt.mew,alpha=pt.alpha,zorder=pt.zorder,\
  ms=pt.ms,ls='None',transform=ccrs.PlateCarree(),label=pt.lab) 

def plottexts(ax,txts,verbose,fontsize):
 if verbose: print('texts now')
 for txt in txts:
  t = ax.text(txt.x,txt.y,txt.lab,fontsize=fontsize,fontstyle=txt.fontstyle,\
  color=txt.color,transform=ccrs.PlateCarree(),ha=txt.ha,va=txt.va) 
  _ = t.set_bbox(dict(facecolor='w', alpha=0.3, edgecolor=None)) 

