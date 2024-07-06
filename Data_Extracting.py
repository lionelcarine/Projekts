import yfinance as yf
import pandas as pd
import json
import matplotlib.pyplot as plt
import requests

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/data/apple.json"


response = requests.get(url)

with open("apple.json", "wb") as file:
    file.write(response.content)


# Load the JSON file
with open('apple.json') as f:
    apple_info = json.load(f)

# Access the 'country' key
print(apple_info['country'])

# Get Apple stock data
apple = yf.Ticker("AAPL")
apple_share_price_data = apple.history(period="max")

# Display first few rows of data
print(apple_share_price_data.head())

# Reset index and plot
apple_share_price_data.reset_index(inplace=True)
apple_share_price_data.plot(x="Date", y="Open")

apple.dividends
apple.dividends.plot()

#plt.show()

# Plot dividends
apple.dividends.plot()
#plt.show()

AMD = yf.Ticker("amd")



