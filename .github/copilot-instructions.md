# GitHub Copilot Instructions

## Context
You are the owner of a small cabin in Island Park, ID.  You want to 
monitor the snow water equivalent (SWE) at your location.  Any SWE greater 
than 10 means you need to shovel the roof.  

The website that shows this is: 
URL: https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1

There are several columns of data.  Give me the most recent values
for Date, Snow Water Equivalent (inches), Snow Depth, and Snow Density.

The value on 11/23/2025 should be 0.0 inches for SWE, -9999.0 for Snow Depth,
0 % for Snow Density.  Find the columns in the table, and extract the most
recent values.

# IMPORTANT: Output ONLY the formatted data in the exact format specified in lines 21-29 below. Do not include any explanation, narrative, or additional text. Just the formatted output.

The format for the output file should be:
```
<if swe greater than 10, add this line>
  Warning: SWE exceeds 10 inches! Action Required!
- Snow Water Equivalent: <swe> inches
- Last Updated: <timestamp in UTC>
- Snow Depth: <depth> inches
- Snow Density: <density> %
- Station: Island Park (ISPI1)
- Source: https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1
```
This data should be saved in a file called `snow_data.txt` in the root of
the repository.  Write the file every day and commit it to the repository.

CRITICAL: Output ONLY the formatted data in the exact format specified in lines 21-29 above. Do not include any explanation, narrative, or additional text. No preamble. No closing remarks. Just the formatted output and nothing else.

- Source: Island Park (ISPI1) snow monitoring station
- URL: https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1
- Data is in an HTML table with columns: Date, Time, Snow Water 
  Equivalent (inches), Snow Depth, Snow Density, Precipitation, 
  Temperature
- Need the most recent (top row) Snow Water Equivalent value
