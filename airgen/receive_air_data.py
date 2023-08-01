# Step 1: Install the necessary libraries
!pip install requests bs4

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

#Fetch the content from the URL
url = "YOUR_URL_HERE"  # Replace with your URL
response = requests.get(url)
html_content = response.text

# Step 3: Parse the content to extract the JSON data
# If the entire page is a JSON response, you can directly load it. 
# If it's embedded in an HTML page, you might need BeautifulSoup to extract it.
soup = BeautifulSoup(html_content, 'html.parser')
# Assuming the JSON data is within a <script> tag, you can extract it like this:
script_content = soup.find('script').string  # Adjust the find method if there are multiple <script> tags
data_dict = json.loads(script_content)

# Convert the JSON data into a DataFrame
# (Using the previous code to transform the data into a DataFrame)
data_points = data_dict['list']
formatted_data = []
for point in data_points:
    dt = datetime.fromtimestamp(point['dt'], tz=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))
    formatted_data.append({
        'co': point['components']['co'],
        'no': point['components']['no'],
        'o3': point['components']['o3'],
        'so2': point['components']['so2'],
        'pm2_5': point['components']['pm2_5'],
        'pm10': point['components']['pm10'],
        'nh3': point['components']['nh3'],
        'hour': dt.hour,
        'year': dt.year,
        'month': dt.month,
        'day': dt.day
    })
df = pd.DataFrame(formatted_data)

print(df)
