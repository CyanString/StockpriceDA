"""
For this project the main script file have application:
1. allow user to input the stock price data
2. allow user to input the period of the RSI
3. allow user to input the indicators of the RSI
4. generate the RSI plot
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from RSI import generate_rsi_plot
from Fibonacci import fibonacci_plot
from swing import swing_plot

DIR = 'stockprice_data/'
FILES_DATA = ['NVIDIA Stock Price History.csv', 'Meta Platforms Stock Price History.csv',
              'Microsoft Stock Price History.csv','Tesla Stock Price History.csv' ]

class TrendlineAnalyser:

    def __init__(self):
        pass

    def load_data(self, filename):
        pass

    def setMethod(self, name):
        pass

    def detectSwing(self):
        pass

    def plot(self):
        pass

    def detectTrend(self):
        pass
    

    def plotTrend(self):
        pass

    def analyze(self):
        pass


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

    fibonacci_plot(stock_data,start_date='2024-01-01')

    swing_plot(stock_data,start_date='2024-10-01',trendline_method= "moving_average")



