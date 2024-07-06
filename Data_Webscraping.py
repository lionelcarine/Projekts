import pandas as pd
import requests
from bs4 import BeautifulSoup

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

url =" https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"

data  = requests.get(url).text
print(data)

soup = BeautifulSoup(data, 'html5lib')
amazon_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])

# First we isolate the body of the table which contains all the information
# Then we loop through each row and find all the column values for each row

amazon_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])

for row in soup.find("tbody").find_all("tr"):
    col = row.find_all("td")
    date = col[0].text.strip().replace(',', '') #ADD_CODE
    Open = col[1].text.strip().replace(',', '')  #ADD_CODE
    high = col[2].text.strip().replace(',', '')  #ADD_CODE
    low =  col[3].text.strip().replace(',', '')  #ADD_CODE
    close = col[4].text.strip().replace(',', '')  #ADD_CODE
    adj_close = col[5].text.strip().replace(',', '') #ADD_CODE
    volume = col[6].text.strip().replace(',', '') #ADD_CODE
    
#amazon_data = amazon_data.append({"Date":date, "Open":Open, "High":high, "Low":low, "Close":close, "Adj Close":adj_close, "Volume":volume}, ignore_index=True)

amazon_data.head()
print(amazon_data.head())
#read_html_pandas_data = pd.read_html(url)
#read_html_pandas_data = pd.read_html(str(soup))
#netflix_dataframe = read_html_pandas_data[0]
#netflix_dataframe.head()
amazon_data.columns.tolist()
last_open = amazon_data.iloc[-1]["Open"]
print("Open value of the last row:", last_open)
