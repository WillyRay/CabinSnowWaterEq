I'll fetch the snow data from the NOAA website and extract the most recent values.

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
# Look for the table that contains the snow data
tables = soup.find_all('table')

# Find the correct table by looking for one with "Snow Water Equivalent" in the headers
data_table = None
for table in tables:
    if 'Snow Water Equivalent' in str(table):
        data_table = table
        break

if data_table:
    # Find all rows in the table
    rows = data_table.find_all('tr')
    
    # Find the header row to identify column positions
    header_row = None
    for row in rows:
        if 'Snow Water Equivalent' in str(row):
            header_row = row
            break
    
    # Get column indices
    headers = header_row.find_all(['th', 'td'])
    swe_col = None
    depth_col = None
    density_col = None
    date_col = None
    time_col = None
    
    for i, header in enumerate(headers):
        header_text = header.get_text().strip()
        if 'Date' in header_text:
            date_col = i
        elif 'Time' in header_text:
            time_col = i
        elif 'Snow Water Equivalent' in header_text:
            swe_col = i
        elif 'Snow Depth' in header_text and 'Density' not in header_text:
            depth_col = i
        elif 'Snow Density' in header_text:
            density_col = i
    
    # Find the first data row (most recent)
    data_row = None
    for row in rows[1:]:  # Skip header row
        cells = row.find_all(['td'])
        if cells and len(cells) > max([swe_col, depth_col, density_col]):
            # Check if this row has actual data
            try:
                swe_text = cells[swe_col].get_text().strip()
                if swe_text and swe_text != '' and not 'Snow Water' in swe_text:
                    data_row = cells
                    break
            except:
                continue
    
    if data_row:
        # Extract values
        date = data_row[date_col].get_text().strip() if date_col else "N/A"
        time = data_row[time_col].get_text().strip() if time_col else "N/A"
        swe = float(data_row[swe_col].get_text().strip())
        depth = data_row[depth_col].get_text().strip() if depth_col else "N/A"
        density = data_row[density_col].get_text().strip() if density_col else "N/A"
        
        # Format timestamp
        timestamp = f"{date} {time} UTC"
