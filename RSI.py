"""
This RSI script file will contain the
RSI function (not done yet)
generate_rsi_plot function
which will show you the date of the stock cross the rsi line(not done)
and provide you the general plot of rsi
"""

import pandas as pd
import matplotlib.pyplot as plt

def generate_rsi_plot(stock_data, price_column, date_column, period=14, indicators=(30, 70), stock_name="Stock"):

    # Calculate the daily price change
    delta = stock_data[price_column].diff(1).dropna()

    # Separate positive and negative changes
    up = delta.copy()
    down = delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # Calculate the rolling average of gains and losses
    avg_gain = up.rolling(window=period).mean()
    avg_loss = abs(down.rolling(window=period).mean())

    # Calculate RSI
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))

    # Add RSI to the stock_data DataFrame
    stock_data['RSI'] = rsi

    # Plot the RSI
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data[date_column], stock_data['RSI'], label='RSI', color='b')
    for i in indicators:
        plt.axhline(y=i, color='r', linestyle='--', alpha=0.5)
    plt.title(f'{stock_name} RSI')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.legend()
    plt.show()

    return stock_data










