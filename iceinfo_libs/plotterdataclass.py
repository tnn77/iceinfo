from dataclasses import dataclass
@dataclass
class xydata:
 """ 
 data class for plotting xy data
 required parameters: x,y,lab
 y0 and y1 are spread
 """
 clr='tab:blue'
 x: list
 y: list
 y0: list=None
 y1: list=None
 lab: str=None
 alpha: float=0.8
 color: str=clr
 mfc: str=clr
 mec: str=clr
 mew: int=2
 ms: int=30
 lw: int=3
 style: str='o'
 ls: str='-'
 fontstyle: str='oblique'
 zorder: int=3
 ha: str='center' # right,left
 va: str='center' # top,bottom,baseline

@dataclass
class grddata:
 """ 
 data class for plotting xyz data
 required parameters: x,y,lab
 optional: alpha=0.7,vlim=[None,None],cmap=None(colormap obj)
 """
 x: list
 y: list
 z: list
 lab: str
 alpha: float=1.0 # use with care as grid lines may show up on the figure.
 vlim: tuple=(None,None)
 cmap: type=None
 zorder: int=1
 normalize: type=None
 s: int=8
 colorbar: bool=True

@dataclass
class vecdata:
 """ 
 data class for plotting xyz data
 required parameters: x,y,z,lab(xpos,ypos,keylength,lab), and 
 vecargs: color,scale_units, scale, width, headwidth, headlength, regrid_shape, pivot
 """
 x: list
 y: list
 u: list
 v: list
 lab: tuple=(0.8,0.9,1,'default') #eg lab '5 $\mathrm{ms}^{-1}$ wind vector'
 labpos: str='E'
 labcoord: str='figure'
 color: str='0.3'
 scale_units: str='xy'
 scale: float=4.5e-5
 width: float=1e-3
 headwidth: float=30
 headlength: float=20
 regrid_shape: int=12
 pivot: str='mid'
 zorder: int=2
 lw: float=1
 ec: str='None'

@dataclass
class cntrdata:
 """ 
 data class for plotting contour data
 required parameters: x,y,cnts,lstyle,labformat
 """
 x: list
 y: list
 z: list
 cntrs: list
 lstyle: list
 labformat: str='%1.2f' # eg. '%d$^\circ$C'
 lw: int=2
 color: str='0.1'
 alpha: float=0.8
 zorder: int=1
