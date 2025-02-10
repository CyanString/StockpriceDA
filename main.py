"""
This main file take the core function of the project which will
give several strategy and provide the proper explanation
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from RSI import generate_rsi_plot


DIR = 'stockprice_data/'
FILES_DATA = ['NVIDIA Stock Price History.csv', 'Meta Platforms Stock Price History.csv',
              'Microsoft Stock Price History.csv','Tesla Stock Price History.csv' ]

for file in FILES_DATA:
    # change the date to the special datetime form and then sort it by the Date
    stock_data= pd.read_csv(os.path.join(DIR, file))
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data = stock_data.sort_values('Date')

    generate_rsi_plot(
        stock_data = stock_data,
        price_column = 'Price',
        date_column = 'Date',
        period=14,
        indicators=(30, 70),
        stock_name=file.split(' ')[0]

    )




