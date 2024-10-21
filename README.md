# iceinfo
## environment
I use (mini)conda, and have not had many dependency issues.  
The conda packages needed are:
- click-help-colors
- cartopy
- pandas
- scipy
- cmocean
- netCDF4
- eccodes 

eccodes is the ECMWF grib tools, which includes the grib\_to\_netcdf command.  
note that some numpy dtype warning appeared when I tested from scratch, but it did not affect the plotting.  
## workflow
$bash do\_ecmwf.sh
--> will call grib\_to\_netcdf to convert grib2 files to the netCDF format. 
--> will call "plotECMWF-LHB.py" to do the wind and pressure field fig, "plotECMWFWave-LHB.py" to do the wave field figure. 
-----> the main python code calls libraries from the iceinfo-libs folder. 

## file managements
This is obviously a preference, so this is just a comment.   
In the Thunderbird app, I used the FiltaQuilla add-on to automatically save attachments to a specific directory (new files).  
After I do the new plots on the latest files, I moved the grib2 and converted NC files to an archive folder.  
I used to rsync the archive figures folders with the Shirase shared directory, so the forecast figures can be uploaded to the NME intranet page.  
