import pandas as pd
import matplotlib.pylab as plt
import numpy as np
from pyodide.http import pyfetch

async def download(url, filename):
    response = await pyfetch(url)
    if response.status == 200:
        with open(filename, "wb") as f:
            f.write(await response.bytes())

file_path="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"
await download(file_path, "usedcars.csv")
file_name="usedcars.csv"
df = pd.read_csv(filename, names = headers)

df.head()


df.replace("?", np.nan, inplace = True)  # replace "?" to NaN
df.head(5)

missing_data = df.isnull()
missing_data.head(5)

for column in missing_data.columns.values.tolist():
    print(column)
    print (missing_data[column].value_counts())
    print("")    


