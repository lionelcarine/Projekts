# Importing the required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime
import lxml
url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
#table_attribs =
# Function to log progress
def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    with open('code_log.txt', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} : {message}\n")


# Function to extract data from the website
def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': table_attribs})
    df = pd.read_html(str(table))[0]
    df = df[['Bank name', 'Market cap(US$ billion)']]
    df.columns = ['Name', 'MC_USD_Billion']
    df['MC_USD_Billion'] = df['MC_USD_Billion'].apply(lambda x: float(x.rstrip('\n')))
    log_progress("Data extraction complete. Initiating Transformation process")
    return df
# Function to transform the dataframe with additional currency columns
def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    exchange_rates = pd.read_csv(csv_path).set_index('Currency').to_dict()['Rate']
    df['MC_GBP_Billion'] = [np.round(x * exchange_rates['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * exchange_rates['EUR'], 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * exchange_rates['INR'], 2) for x in df['MC_USD_Billion']]
    log_progress("Data transformation complete. Initiating Loading process")
    return df


# Function to load dataframe to CSV
def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_path, index=False)
    log_progress("Data saved to CSV file")


# Function to load dataframe to SQL database
def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
    log_progress("Data loaded to Database as a table, Executing queries")


# Function to run a query on the database
def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    result = pd.read_sql_query(query_statement, sql_connection)
    print(result)
    log_progress("Process Complete")


# Main script execution
if __name__ == "__main__":
    log_progress("Preliminaries complete. Initiating ETL process")


    # Known values
    data_url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
    exchange_rate_csv_path = "exchange_rate.csv"
    output_csv_path = "./Largest_banks_data.csv"
    db_name = "Banks.db"
    table_name = "Largest_banks"


    # Extract data
    df = extract(data_url, "wikitable sortable")


    # Transform data
    df = transform(df, exchange_rate_csv_path)
    print(df['MC_EUR_Billion'][4])  # This is for the quiz question


    # Load data to CSV
    load_to_csv(df, output_csv_path)


    # Load data to SQL database
    conn = sqlite3.connect(db_name)
    log_progress("SQL Connection initiated")
    load_to_db(df, conn, table_name)


    # Run query on the database
    run_query("SELECT * FROM Largest_banks", conn)
    run_query("SELECT AVG(MC_USD_Billion) FROM Largest_banks", conn)
    run_query("SELECT Name FROM Largest_banks LIMIT 5", conn)


    # Close SQL connection
    conn.close()
    log_progress("Server Connection closed")