import yfinance as yf
import pandas as pd
import json
import matplotlib.pyplot as plt
import requests


AMD = yf.Ticker("amd")
url= "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/data/amd.json"

response1 = requests.get(url)

with open("amd.json", "wb") as file:
    file.write(response1.content)

with open('amd.json') as json_file:
    amd_info = json.load(json_file)
    # Print the type of data variable    
    #print("Type:", type(apple_info))
#amd_info
print("Type:", type(amd_info))

country = amd_info.get('country')
sector = amd_info.get('sector')

print(f"Country: {country}")
print(f"Sector: {sector}")

amd_history = AMD.history(period="max")

# Display the first row to get the volume traded on the first day
Volume = amd_history.iloc[0]['Volume']

print(f"Volume traded on the first day: {Volume}")
