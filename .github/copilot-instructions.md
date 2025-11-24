# GitHub Copilot Instructions

## Context
You are the owner of a small cabin in Island Park, ID.  You want to 
monitor the snow water equivalent (SWE) at your location.  Any SWE greater 
than 10 means you need to shovel the roof.  

The website that shows this is: 
https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1

There are several columns of data.  Give me the most recent values
for Date, Snow Water Equivalent (inches), Snow Depth, and Snow Density.

The format for the output file should be:
```
<if swe greater than 10, add this line>
  Warning: SWE exceeds 10 inches! Action Required!
Snow Water Equivalent: <value> inches
Last Updated: <timestamp in UTC>
Snow Depth: <value> inches
Snow Density: <value> %
Station: Island Park (ISPI1)
Source: https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1
```
This data should be saved in a file called `snow_data.txt` in the root of
the repository.  Write the file every day and commit it to the repository.



- Source: Island Park (ISPI1) snow monitoring station
- URL: https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1
- Data is in an HTML table with columns: Date, Time, Snow Water 
  Equivalent (inches), Snow Depth, Snow Density, Precipitation, 
  Temperature
- Need the most recent (top row) Snow Water Equivalent value
