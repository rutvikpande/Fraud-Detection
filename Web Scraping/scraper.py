# # Import required modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# Headers
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

# Columns
columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

# Stocks
stock_codes = ["TCS", "AAPL","AMZN","GOOG","MSFT","AMD","INTC","FB","NFLX","TTM","ITC.NS",
"HDB","INFY","SBIN.NS","WIPRO.NS","HPE","DELL","LNVGY"]

# Generate required url
def generate_url(stockcode):
    url = "https://finance.yahoo.com/quote/" + stockcode + "/history?p=" + stockcode
    return url

# Generate raw data
def generate_raw(url):
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, 'html5lib')
    table = soup.findAll('tr', attrs = {'class':'BdT'})
    return table

# Get the relevant fields
def getFields(record):
    data = record.findAll('span')
    processed_record = []
    for item in data:
        processed_record.append(item.decode_contents())
    return processed_record

# Build a dataframe from table
def get_df_from_table(table):
    df = pd.DataFrame(columns=columns)
    records = []
    for record in table:
        records.append(getFields(record))

    df = df.append(pd.DataFrame(records, columns=columns), ignore_index = True)
    return df

# Driver Code
for stock in stock_codes:
    url = generate_url(stock)
    table = generate_raw(url)
    df = get_df_from_table(table)
    df.to_csv(f'./{stock}_data.csv')