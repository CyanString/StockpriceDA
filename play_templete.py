import urllib.request
import os
import pandas as pd
from indicator import *

# this is strange, It seems that my the www.investing.com have some token to download the data, so I have no idea how
# to simply download data from url. I could try to use the web scraping but I am not sure is that really what we need


DIR = 'stockprice_data/'
FILES_DATA = ['NVIDIA Stock Price History.csv', 'Meta Platforms Stock Price History.csv',
              'Microsoft Stock Price History.csv','Tesla Stock Price History.csv' ]


for file in FILES_DATA:
    # change the date to the special datetime form and then sort it by the Date

    stock_data= pd.read_csv(os.path.join(DIR, file))
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data = stock_data.sort_values('Date')
    print(file)
    generate_signals(stock_data)
    signal_plot(stock_data)
    calculate_return(stock_data)

