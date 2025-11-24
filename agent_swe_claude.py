import os
import time
import requests
from typing import Optional

# Read instructions from the specified markdown file
with open('.github/copilot-instructions.md', 'r') as f:
    instructions = f.read()

# Hard-coded target URL for Island Park (ISPI1) station
url = "https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1"

def fetch_page(url: str) -> str:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text

web_text = fetch_page(url)

# Set up the Claude API (Anthropic)
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    print("Missing ANTHROPIC_API_KEY environment variable.")
    exit(1)

headers = {
    'x-api-key': api_key,
    'anthropic-version': '2023-06-01',
    'content-type': 'application/json'
}

# Prepare the payload for the Claude API
prompt = f"""You are extracting structured snow data for Island Park (ISPI1).
Return ONLY the following exact format (no extra commentary):
<warning line if SWE > 10>
Snow Water Equivalent: <swe> inches
Last Updated: <UTC timestamp>
Snow Depth: <depth> inches
Snow Density: <density> %
Station: Island Park (ISPI1)
Source: https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1

If SWE <= 10 omit the warning line entirely. Use the most recent row (top
of table). If a field is missing use the sentinel values specified in the
instructions. Timestamp should be current UTC now in ISO-like
YYYY-MM-DD HH:MM:SS UTC.
Do not include markdown fences.
Page HTML below:
{web_text}
"""

payload = {
    'model': 'claude-3-5-sonnet-20241022',
    'max_tokens': 800,
    'messages': [
        {'role': 'user', 'content': prompt}
    ]
}

# Call the Claude API to extract SWE
def call_claude(payload: dict, retries: int = 3, backoff: float = 2.0) -> Optional[str]:
    for attempt in range(1, retries + 1):
        resp = requests.post('https://api.anthropic.com/v1/messages', headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            if 'content' in data and data['content'] and 'text' in data['content'][0]:
                return data['content'][0]['text']
            print("Unexpected response structure, content missing.")
            return None
        else:
            print(f"Attempt {attempt} failed: {resp.status_code} {resp.text[:200]}")
            if resp.status_code == 401:
                print("Authentication error - check ANTHROPIC_API_KEY secret.")
                return None
            time.sleep(backoff * attempt)
    return None

result = call_claude(payload)
if not result:
    print("Failed to obtain result from Claude.")
    exit(1)

# Output the result to snow_data.txt
final_text = result.strip()
# Basic sanitation: remove enclosing code fences if accidentally added
if final_text.startswith('```'):
    final_text = final_text.strip('`')
with open('snow_data.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(final_text + '\n')
print("snow_data.txt written")
