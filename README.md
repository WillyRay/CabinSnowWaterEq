I'll help you extract the snow data from the NOAA website. Let me fetch the current data and format it according to your specifications.

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

# Fetch the webpage
url = "https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the data table
table = soup.find('pre')  # The data is typically in a pre-formatted text block
if table:
    lines = table.text.strip().split('\n')
    
    # Find the header line and data lines
    data_started = False
    header_indices = {}
    
    for i, line in enumerate(lines):
        # Look for the header line containing column names
        if 'Snow Water Equivalent' in line or 'SWE' in line:
            # Parse header positions
            header_line = line
            header_indices['date'] = line.find('Date')
            header_indices['swe'] = line.find('Snow Water Equivalent')
            if header_indices['swe'] == -1:
                header_indices['swe'] = line.find('SWE')
            header_indices['depth'] = line.find('Snow Depth')
            header_indices['density'] = line.find('Snow Density')
            data_started = True
            continue
            
        # Get the first data row after headers
        if data_started and re.match(r'\d{2}/\d{2}/\d{4}', line.strip()[:10]):
            # Parse the data line based on column positions
            date_str = line[:10].strip()
            
            # Extract SWE value (typically in column around position 20-30)
            swe_match = re.search(r'(\d+\.\d+|-?\d+\.?\d*)\s+', line[20:35])
            swe = float(swe_match.group(1)) if swe_match else 0.0
            
            # Extract Snow Depth (typically after SWE)
            depth_match = re.search(r'(\d+\.\d+|-?\d+\.?\d*)\s+', line[35:50])
            depth = float(depth_match.group(1)) if depth_match else -9999.0
            
            # Extract Snow Density (typically after Snow Depth)
            density_match = re.search(r'(\d+\.?\d*|-?\d+)', line[50:65])
            density = int(float(density_match.group(1))) if density_match else 0
            
            # Get current UTC time
            utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            
            # Format output
            output_lines = []
            if swe > 10:
                output_lines.append("Warning: SWE exceeds 10 inches! Action Required!")
            output_lines.append(f"- Snow Water Equivalent: {swe} inches")
            output_lines.append(f"- Last Updated: {utc_time}")
            output_lines.append(f"- Snow

## Project Description

This repository monitors the snow water equivalent (SWE) at a small cabin in Island Park, Idaho. The SWE data is automatically fetched daily from the NOAA Island Park (ISPI1) snow monitoring station.

### Purpose
Monitor snow conditions to determine when roof shoveling is needed. A warning is issued when SWE exceeds 10 inches.

### Data Source
- Station: Island Park (ISPI1)
- URL: https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1
- Data updated daily at 06:00 Mountain Time

### Data Fields
- **Snow Water Equivalent (SWE)**: Water content of the snowpack in inches
- **Snow Depth**: Total depth of snow in inches
- **Snow Density**: Ratio of water weight to snow volume as a percentage
- **Last Updated**: UTC timestamp of the most recent measurement
