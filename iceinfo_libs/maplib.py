"""
Created on # Y/m/d

@author:
Notes:
plot map library. imports functions from mapfunc.py

"""

import numpy as np

import matplotlib as mpl
# mpl.use('svg')
# mpl.use('pdf')
mpl.use('agg')
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.ticker as ticker

import cartopy.crs as ccrs
# from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeat

### local libs
from iceinfo_libs.mapfunc import plotvector,plotcontour,plottracks,plotpoints,plottexts
from iceinfo_libs.scale_bar import scale_bar 

################################################################################
### optional arguments that can be updated
# can add coast and land properties too.
kwargs = dict(
   coastison=False,coastlw=4,coastlc='k',
   landison=False,landalpha=0.4,
   lonlatison={"bottom": "x", "left": "y"},
   legloc='best',legend=2,legms=None,leglw=None,
   cbarextend='neither',cbarticks=None,
   bgcolor='w',
   )
   
sclbar_args=dict(family='serif',lw=5,loc=(0.05,0.05),len=100,color='k',metres_per_unit=1000,unit_name="km")

inset_args=dict(width="15%", height="35%", loc='upper right',\
  extent=[-1,1,-69,-68],central_lon=37.8,grd=[])
################################################################################

def plotmapfig(
 txts,pts,trcks,grd,vec,vec2,cntr,scat,\
 figsize,dpi,facecolor,edgecolor,fontsize,\
 central_longitude,plt_extent,lat_tiks,lon_tiks,\
 title,fout,verbose,
 projection,circle=[],inset=False,scalebar=False,\
 ):
 """takes various input data to plot"""
 f = plt.figure(figsize=figsize,dpi=dpi,facecolor=facecolor,edgecolor=edgecolor)
 ax = plt.subplot(1,1,1,projection=projection)
 _ = ax.set_extent(plt_extent, crs=ccrs.PlateCarree(central_longitude=central_longitude))
 ### do plot for each data
 if verbose: print('grid now')
 ### if there are no gridded or scatter data to show in color, make a background map image.
 if not any([grd,scat]):  _ = ax.stock_img()
 if grd:
  pcm = ax.pcolormesh(grd.x,grd.y,grd.z,cmap=grd.cmap,\
    transform=ccrs.PlateCarree(),zorder=grd.zorder,alpha=grd.alpha,\
    shading='auto',vmin=grd.vlim[0],vmax=grd.vlim[1]) 
  if grd.colorbar: grd.pcm = pcm
 if scat:
  pcm = ax.scatter(scat.x,scat.y,c=scat.z,cmap=scat.cmap,s=scat.s,marker=".",\
    transform=ccrs.PlateCarree(),zorder=scat.zorder,alpha=scat.alpha,\
    vmin=scat.vlim[0],vmax=scat.vlim[1],norm=scat.normalize) 
  # kind of assumes either scatter markers or grid data
  if scat.colorbar: scat.pcm = pcm
 #
 if verbose: print('features now')
 if kwargs.get('coastison'): _=ax.coastlines(resolution='50m',zorder=1,\
 lw=kwargs.get('coastlw'),color=kwargs.get('coastlc'))
 if kwargs.get('landison'): _= ax.add_feature(cfeat.LAND,zorder=1,\
 facecolor=cfeat.COLORS['land_alt1'],alpha=kwargs.get('landalpha'))
 # facecolor='0.9',alpha=kwargs.get('landalpha'))
 ### vectors ###
 if vec: _ = plotvector(ax,vec,verbose,fontsize)
 if vec2: _ = plotvector(ax,vec2,verbose,fontsize)
 ### contours ###
 if cntr: _ = plotcontour(ax,cntr,verbose,fontsize)
 ### tracks ###
 if trcks: _ = plottracks(ax,trcks,verbose,fontsize)
 ### points ###
 if pts: _ = plotpoints(ax,pts,verbose,fontsize)
 ### texts ###
 if txts:_ = plottexts(ax,txts,verbose,int(0.75*fontsize))
 ### ### 
 ### tick labels and legends etc.
 if verbose: print('tick labels and legend now')
 legend = kwargs.get('legend')
 if legend:
  leg = ax.legend(loc=kwargs.get('legloc'),fontsize=int(fontsize*0.6),\
    ncol=legend,fancybox=True)
  if kwargs.get('legms') or kwargs.get('leglw'):
   for x in leg.legendHandles:
    if kwargs.get('legms'): x.set_ms(kwargs.get('legms'))
    if kwargs.get('leglw'): x.set_lw(kwargs.get('leglw'))
  _ = leg.get_frame().set_alpha(0.5)
 ### scale bar
 text_kwargs = dict(family=sclbar_args.get('family'),size=fontsize)
 plot_kwargs = dict(linewidth=sclbar_args.get('lw')) 
 if scalebar: _ = scale_bar(ax,sclbar_args.get('loc'),\
  sclbar_args.get('len'),color=sclbar_args.get('color'),\
  metres_per_unit=sclbar_args.get('metres_per_unit'),\
  unit_name=sclbar_args.get('unit_name'),\
  text_kwargs=text_kwargs,plot_kwargs=plot_kwargs)
 ### axes ticks
 xticks = lon_tiks.tolist()
 yticks = lat_tiks.tolist()
 gl = ax.gridlines(xlocs=xticks, ylocs=yticks,\
 draw_labels=kwargs.get('lonlatison'),x_inline=False,y_inline=False, \
 linestyle='--', color='k', alpha=0.5, linewidth=0.5)
 gl.n_steps = 90
 gl.xformatter = LONGITUDE_FORMATTER;gl.yformatter = LATITUDE_FORMATTER
 gl.rotate_labels = False
 gl.right_labels = gl.top_labels = False
 gl.ylocator = ticker.FixedLocator(yticks);gl.xlocator = ticker.FixedLocator(xticks)
 gl.ylabel_style = gl.xlabel_style = {'size': int(fontsize*0.75), 'color': 'gray'}
 #
 if verbose: print('color bar now')
 if any([grd,scat]):
  for xx in [grd,scat]:
   if xx:
    if xx.colorbar:
     pcm = xx.pcm; lab = xx.lab
     cbar = plt.colorbar(pcm,ticks=kwargs.get('cbarticks'),extend=kwargs.get('cbarextend'),aspect=50,fraction=0.01,pad=0.01)
     _ = cbar.ax.get_yaxis().labelpad = 30
     _ = cbar.ax.set_ylabel(lab,rotation=270,fontsize=fontsize)
     _ = cbar.ax.tick_params(labelsize=int(fontsize*0.75)) #'large')
     _ = cbar.ax.minorticks_on()
 #
 ### draw a circle in axes coordinates, used when showing Arctic/Antarctica in a circular shape.
 if circle: _ = ax.set_boundary(circle, transform=ax.transAxes)
 #
 _ = plt.title(title,fontsize=int(0.7*(fontsize)))
 if inset:
  ### https://stackoverflow.com/questions/55385515/embed-small-map-cartopy-on-matplotlib-figure ###
  ### alternate option, https://notebook.community/ueapy/ueapy.github.io/content/notebooks/2019-05-30-cartopy-map ###
  import cartopy.mpl.geoaxes
  from mpl_toolkits.axes_grid1.inset_locator import inset_axes
  axins = inset_axes(ax,width=inset_args.get('width'),\
    height=inset_args.get('height'), loc=inset_args.get('loc'), 
    axes_class=cartopy.mpl.geoaxes.GeoAxes, 
    axes_kwargs=dict(projection=projection))
  if sar:
   _ = plotsar(axins,sar,verbose)
  else: _ = axins.stock_img()
  if cntr: _ = plotcontour(axins,cntr,verbose,fontsize)
  if trcks: _ = plottracks(axins,trcks,verbose,fontsize)
  ### points ###
  if pts: _ = plotpoints(axins,pts,verbose,fontsize)
  _ = axins.set_extent(inset_args.get('extent'),\
    crs=ccrs.PlateCarree(central_longitude=inset_args.get('central_lon')))

 if verbose: print('saving now')
 plt.savefig(fout,bbox_inches='tight')
 if verbose: print('closing now')
 plt.close(f)

def plotmercator(txts=[],pts=[],trcks=[],grd=[],\
   vec=[],vec2=[],cntr=[],scat=[],img=[],sar=[],\
   figsize = (15,12),dpi = 100,facecolor='w',edgecolor='k',fontsize=18,
   central_longitude = 0,central_latitude = 0,plt_extent = [-180,180,60,90],
   lat_tiks = np.arange(50.,89.,5.),lon_tiks = np.arange(-180,181,15),
   title=None,fout = 'test',verbose=False,inset=False,scalebar=False,
   **kwargin):
 #
 ### update kw options
 kwargs.update(kwargin)
 if scalebar:
  sclbar_args.update(scalebar)
 projection=ccrs.Mercator()
 _ = plotmapfig(
 txts,pts,trcks,grd,vec,vec2,cntr,scat,
 figsize,dpi,facecolor,edgecolor,fontsize,
 central_longitude,plt_extent,lat_tiks,lon_tiks,
 title,fout,verbose,
 projection=projection,inset=inset,scalebar=scalebar,
 )

def plotpolarstereo(txts=[],pts=[],trcks=[],grd=[],\
  vec=[],vec2=[],cntr=[],scat=[],img=[],sar=[],\
  figsize = (15,12),dpi = 100,facecolor='w',edgecolor='k',fontsize=18,
  central_longitude = 0,central_latitude = 90,plt_extent = [-180,180,60,90],
  lat_tiks = np.arange(50.,89.,5.),lon_tiks = np.arange(-180,181,15),UTM=[],
  title=None,fout = 'test',verbose=False,inset=False,scalebar=False,\
  inset_ts=False,
  **kwargin):
 """used when high res data were available for Totten"""
 # update args (only if dict is provided for optional args.)
 kwargs.update(kwargin)
 if isinstance(scalebar,dict):
  sclbar_args.update(scalebar)
 if isinstance(inset,dict):
  inset_args.update(inset)

 projection=ccrs.Stereographic(central_latitude=central_latitude,central_longitude=central_longitude)
 _ = plotmapfig(
 txts,pts,trcks,grd,vec,vec2,cntr,scat,
 figsize,dpi,facecolor,edgecolor,fontsize,
 central_longitude,plt_extent,lat_tiks,lon_tiks,
 title,fout,verbose,
 projection=projection,inset=inset,scalebar=scalebar,inset_ts=inset_ts,
 )

def plotps(txts=[],pts=[],trcks=[],grd=[],\
   vec=[],vec2=[],cntr=[],scat=[],img=[],sar=[],\
   figsize = (12,12),dpi = 100,facecolor='w',edgecolor='k',fontsize=18,
   central_longitude=0,central_latitude=False,plt_extent=[-180,180,65,90],
   lat_tiks = np.arange(50.,89.,5.),lon_tiks = np.arange(-180,181,15),
   title=None,fout = 'test',verbose=False,hem='n',UTM=[],
   **kwargin):
 """used when Arctic or Antarctica is shown as a circular shape."""
 #
 kwargs.update(kwargin)
 ### draw a circle in axes coordinates
 ### https://scitools.org.uk/cartopy/docs/v0.15/examples/always_circular_stereo.html
 theta = np.linspace(0, 2*np.pi, 100)
 center, radius = [0.5, 0.5], 0.5
 verts = np.vstack([np.sin(theta), np.cos(theta)]).T
 circle = mpath.Path(verts * radius + center)
 projection=ccrs.NorthPolarStereo(central_longitude=central_longitude,globe=None)
 if hem=='s':
  projection=ccrs.SouthPolarStereo(central_longitude=central_longitude,globe=None)
  plt_extent=[-180,180,-90,-50]
  lat_tiks = np.arange(50.,89.,5.)
  lat_tiks = np.arange(-50.,-89.,-5.)
 _ = plotmapfig(
 txts,pts,trcks,grd,vec,vec2,cntr,scat,
 figsize,dpi,facecolor,edgecolor,fontsize,
 central_longitude,plt_extent,lat_tiks,lon_tiks,
 title,fout,verbose,
 projection=projection,circle=circle
 )
