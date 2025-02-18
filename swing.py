import matplotlib.pyplot as plt
import numpy as np


def get_swing_points(stock_data):
    swing_points = []
    # Iterate over the dataset to find high/low points
    
    for i in range(1, len(stock_data) - 1):
        if stock_data['Price'].iloc[i] > stock_data['Price'].iloc[i - 1] and stock_data['Price'].iloc[
            i] > stock_data['Price'].iloc[i + 1]:
            swing_points.append((stock_data['Date'].iloc[i], stock_data['Price'].iloc[i], 'High'))
        elif stock_data['Price'].iloc[i] < stock_data['Price'].iloc[i - 1] and stock_data['Price'].iloc[
            i] < stock_data['Price'].iloc[i + 1]:
            swing_points.append((stock_data['Date'].iloc[i], stock_data['Price'].iloc[i], 'Low'))

    return swing_points


def swing_plot(stock_data, start_date=None, trendline_method='linear_interpolation'):
    if start_date:
        stock_data = stock_data[stock_data['Date'] >= start_date]

    swing_points = get_swing_points(stock_data)
    plt.figure(figsize=(12, 8))
    plt.plot(stock_data['Date'], stock_data['Price'], label='Price', color='blue', linewidth=2)

    swing_high_dates = [point[0] for point in swing_points if point[2] == 'High']
    swing_high_prices = [point[1] for point in swing_points if point[2] == 'High']
    swing_low_dates = [point[0] for point in swing_points if point[2] == 'Low']
    swing_low_prices = [point[1] for point in swing_points if point[2] == 'Low']

    # Plot swing points
    plt.scatter(swing_high_dates, swing_high_prices, color='green', label='Swing Highs', zorder=5)
    plt.scatter(swing_low_dates, swing_low_prices, color='red', label='Swing Lows', zorder=5)

    # Plot trendlines
    if trendline_method == 'linear_interpolation':
        if len(swing_high_dates) > 1:
            plt.plot(swing_high_dates, np.interp(range(len(swing_high_dates)), [0, len(swing_high_dates) - 1],
                                                 [swing_high_prices[0], swing_high_prices[-1]]),
                     linestyle='--', color='black', label='Downtrend')
        if len(swing_low_dates) > 1:
            plt.plot(swing_low_dates, np.interp(range(len(swing_low_dates)), [0, len(swing_low_dates) - 1],
                                                [swing_low_prices[0], swing_low_prices[-1]]),
                     linestyle='--', color='orange', label='Uptrend')
    elif trendline_method == 'linear_regression':
        if len(swing_high_dates) > 1:
            coeffs = np.polyfit(range(len(swing_high_prices)), swing_high_prices, 1)
            trend = np.polyval(coeffs, range(len(swing_high_prices)))
            plt.plot(swing_high_dates, trend, linestyle='--', color='black', label='Downtrend (Regression)')
        if len(swing_low_dates) > 1:
            coeffs = np.polyfit(range(len(swing_low_prices)), swing_low_prices, 1)
            trend = np.polyval(coeffs, range(len(swing_low_prices)))
            plt.plot(swing_low_dates, trend, linestyle='--', color='orange', label='Uptrend (Regression)')
    elif trendline_method == 'polynomial_regression':
        degree = 2
        if len(swing_high_dates) > 1:
            coeffs = np.polyfit(range(len(swing_high_prices)), swing_high_prices, degree)
            trend = np.polyval(coeffs, range(len(swing_high_prices)))
            plt.plot(swing_high_dates, trend, linestyle='--', color='black', label='Downtrend (Poly Reg)')
        if len(swing_low_dates) > 1:
            coeffs = np.polyfit(range(len(swing_low_prices)), swing_low_prices, degree)
            trend = np.polyval(coeffs, range(len(swing_low_prices)))
            plt.plot(swing_low_dates, trend, linestyle='--', color='orange', label='Uptrend (Poly Reg)')
    elif trendline_method == 'moving_average':
        window = 5
        if len(swing_high_prices) > window:
            moving_avg_high = np.convolve(swing_high_prices, np.ones(window) / window, mode='valid')
            plt.plot(swing_high_dates[window - 1:], moving_avg_high, linestyle='--', color='black',
                     label='Downtrend (MA)')
        if len(swing_low_prices) > window:
            moving_avg_low = np.convolve(swing_low_prices, np.ones(window) / window, mode='valid')
            plt.plot(swing_low_dates[window - 1:], moving_avg_low, linestyle='--', color='orange', label='Uptrend (MA)')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Price with Trendlines and Swing Points')
    plt.legend()
    plt.grid()
    plt.show()
