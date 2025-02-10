import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# this function here is to calculate the fibonacci levels
def fibonacci_levels(data):
    max_price = data['Price'].max()
    min_price = data['Price'].min()
    diff = max_price - min_price
    levels = {
        '0%': max_price,
        '23.6%': max_price - diff * 0.236,
        '38.2%': max_price - diff * 0.382,
        '50%': max_price - diff * 0.5,
        '61.8%': max_price - diff * 0.618,
        '78.6%': max_price - diff * 0.786,
    }
    return levels

def get_fibonacci_levels(price,fibonacci_levels):
    upper_level = min(levels for levels in fibonacci_levels.values() if levels >= price)
    lower_level = max(levels for levels in fibonacci_levels.values() if levels <= price)
    return upper_level, lower_level





def fibonacci_plot(stock_data):
    levels = fibonacci_levels(stock_data)
    fig, ax = plt.subplots()
    ax.plot(levels['0%'], levels['23.6%'])
    ax.plot(levels['0%'], levels['38.2%'])
    ax.plot(levels['0%'], levels['50%'])
    ax.plot(levels['0%'], levels['61.8%'])
    ax.plot(levels['0%'], levels['78.6%'])

    plt.figure(figsize=(10, 6))
    plt.plot(stock_data[date_column], stock_data['RSI'], label='RSI', color='b')
    for i in indicators:
        plt.axhline(y=i, color='r', linestyle='--', alpha=0.5)
    plt.title(f'{stock_name} RSI')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.legend()
    plt.show()

