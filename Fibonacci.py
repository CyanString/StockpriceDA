import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# this function here is to calculate the fibonacci levels
def calculate_fibonacci_levels(data):
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
    upper_level = min([levels for levels in fibonacci_levels.values() if levels >= price],default=None)
    lower_level = max([levels for levels in fibonacci_levels.values() if levels <= price],default=None)
    return upper_level, lower_level


def fibonacci_plot(stock_data, start_date=None):
    # Filter stock data by the specified start date
    if start_date:
        stock_data = stock_data[stock_data['Date'] >= start_date]

    # Calculate Fibonacci levels
    fibonacci_levels = calculate_fibonacci_levels(stock_data)

    plt.figure(figsize=(12, 8))

    # Plot the price data
    plt.plot(stock_data['Date'], stock_data['Price'], label='Price', color='blue', linewidth=2)
    # Plot the Fibonacci levels as horizontal lines
    for level, value in fibonacci_levels.items():
        plt.hlines(value, xmin=stock_data['Date'].min(), xmax=stock_data['Date'].max(), label=f'Fibonacci {level}',
                   linestyle='dashed')
    # Add labels, title, and legend
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price', fontsize=14)
    plt.legend(loc='best', fontsize=12)
    plt.grid()
    plt.show()


