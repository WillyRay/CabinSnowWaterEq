import os
import requests

# Read instructions from the specified markdown file
with open('.github/copilot-instructions.md', 'r') as f:
    instructions = f.read()

# Hard-coded target URL for Island Park (ISPI1) station
url = "https://www.nwrfc.noaa.gov/snow/snowplot.cgi?ISPI1"

# Get the web page text
response = requests.get(url)
web_text = response.text

# Set up the Claude API
api_key = os.getenv('ANTHROPIC_API_KEY')
headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

# Prepare the payload for the Claude API
payload = {
    'model': 'claude-3-5-sonnet-20241022',
    'max_tokens': 1000,
    'messages': [
        {
            'role': 'user',
            'content': f'{instructions}\n\nPage Text:\n{web_text}'
        }
    ]
}

# Call the Claude API to extract SWE
response = requests.post('https://api.anthropic.com/v1/messages', headers=headers, json=payload)

# Check for errors in the response
if response.status_code != 200:
    print(f"API Error: {response.status_code}")
    print(f"Response: {response.text}")
    exit(1)

response_json = response.json()
if 'error' in response_json:
    print(f"API Error: {response_json['error']}")
    exit(1)

result = response_json['content'][0]['text']

# Output the result to snow_data.txt
with open('snow_data.txt', 'w') as output_file:
    output_file.write(result.strip())
