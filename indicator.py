import matplotlib.pyplot as plt
import numpy as np


#create the function to calculate rsi

def calculate_rsi(data, period = 14):
    delta = data['Price'].diff()
    gain =(delta.where(delta > 0,0)).rolling(window=period).mean()
    loss =(-delta.where(delta < 0,0)).rolling(window=period).mean()
    relative_strength = gain / loss
    rsi = 100 - 100 / (1 + relative_strength)
    return rsi

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



def generate_signals(data):
    data['RSI'] = calculate_rsi(data)
    fibonacci_levels = calculate_fibonacci_levels(data)
    buy_signals = []
    sell_signals = []
    position = False

    for i in range(len(data)):
        if i == 0:  # Skip the first row to avoid index issues
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)
            continue

        previous_upper_level, previous_lower_level = get_fibonacci_levels(data['Price'].iloc[i-1], fibonacci_levels)

        if previous_upper_level is None or previous_lower_level is None:
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)
            continue

        if data['RSI'].iloc[i] < 50 and data['Price'].iloc[i] <= previous_lower_level and not position:
            buy_signals.append(data['Price'].iloc[i])
            sell_signals.append(np.nan)
            position = True
        elif data['RSI'].iloc[i] > 70 and data['Price'].iloc[i] >= previous_upper_level and position:
            buy_signals.append(np.nan)
            sell_signals.append(data['Price'].iloc[i])
            position = False
        else:
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)

    return buy_signals, sell_signals


# Generate the trading signals

def calculate_return(data):
    data['Buy signals'], data['Sell signals'] = generate_signals(data)
    buy_price = data['Buy signals'].dropna().values
    sell_price = data['Sell signals'].dropna().values
    returns ,i = 0,0
    for buy,sell in zip(buy_price, sell_price):
        print(i,')',sell,'-','buy','=',sell-buy)
        returns += sell-buy
        i += 1
    return returns

def signal_plot(data):
    data['Buy signals'], data['Sell signals'] = generate_signals(data)
    data['RSI'] = calculate_rsi(data)
    fibonacci_levels = calculate_fibonacci_levels(data)
    #plot the stock price and signals
    plt.figure(figsize=(14,7))
    plt.plot(data['Price'], label='Price',alpha=0.5)
    plt.scatter(data.index, data['Buy signals'], label='Buy signals',alpha=0.5,marker='^',color='green')
    plt.scatter(data.index, data['Sell signals'], label='Sell signals',alpha=0.5,marker='v',color='red')

    #add fibonacci retracement levelsto the plot
    for level in fibonacci_levels.values():
        plt.axhline(y = level,color='gray',linestyle='--',alpha=0.5)

    plt.title("Stock price with trading signals")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()



