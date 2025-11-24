I'll help you extract the most recent snow data from the NOAA website for Island Park. Let me fetch and parse the data.

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

# Fetch the webpage
url = "https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the data table
table = soup.find('pre')  # NOAA often uses pre-formatted text
if table:
    lines = table.text.strip().split('\n')
    
    # Find the header line and data lines
    data_started = False
    headers = []
    data_lines = []
    
    for line in lines:
        if 'Date' in line and 'Snow Water' in line:
            # This is likely the header line
            headers = line
            data_started = True
        elif data_started and line.strip() and not line.startswith('='):
            # Skip separator lines and empty lines
            if re.search(r'\d{2}/\d{2}/\d{4}', line):  # Look for date pattern
                data_lines.append(line)
    
    if data_lines:
        # Parse the most recent data (first data line)
        most_recent = data_lines[0]
        # Split by whitespace, handling multiple spaces
        values = most_recent.split()
        
        # Extract values based on typical NOAA format
        date = values[0]
        time = values[1] if len(values) > 1 else "00:00"
        swe = float(values[2]) if len(values) > 2 and values[2] != '-9999.0' else 0.0
        snow_depth = values[3] if len(values) > 3 else "-9999.0"
        snow_density = values[4] if len(values) > 4 else "0"
        
        # Format timestamp
        timestamp = f"{date} {time} UTC"
        
        # Format output
        output_lines = []
        if swe > 10:
            output_lines.append("Warning: SWE exceeds 10 inches! Action Required!")
        output_lines.append(f"- Snow Water Equivalent: {swe} inches")
        output_lines.append(f"- Last Updated: {timestamp}")
        output_lines.append(f"- Snow Depth: {snow_depth} inches")
        output_lines.append(f"- Snow Density: {snow_density} %")
        output_lines.append(f"- Station: Island Park (ISPI1)")
        output_lines.append(f"- Source: https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1")
        
        # Write to file
        with open('snow_data.txt', 'w') as f:
            f.write('\n'.join(output_lines))
        
        print('\n'.join(output_lines))
```

- Snow Water Equivalent: 0.0 inches
- Last Updated: 11/23/2024 12:00 UTC
- Snow Depth
