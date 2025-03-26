import pandas as pd
import numpy as np
import yfinance as yf



def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_ema(data, window):
    return data['Close'].ewm(span=window, adjust=False).mean()


def calculate_plr_slope(data, window=5):
    x = np.arange(window)
    slopes = []
    for i in range(len(data["Close"]) - window + 1):
        y = data["Close"].iloc[i:i + window]
        # weighted plr
        weights = np.linspace(1, 3, window)
        slope = np.polyfit(x, y, 1, w=weights)[0]
        slopes.append(slope)

    slopes = ([np.nan] * (window - 1) + slopes)
    return pd.Series(slopes, index=data.index)

def calculate_atr(data, window=14):
    high = data['High']
    low = data['Low']
    close = data['Close']

    # true TR
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # calculate ATR（SMA）
    atr = tr.rolling(window).mean()
    return atr


def dynamic_exit_rule(data, entry_idx, current_idx, entry_price):
    """
    return：if exit, exit price, reason
    """
    current_close = data['Close'].iloc[current_idx]
    current_profit = (current_close - entry_price) / entry_price

    # dynamic stop（ATR）
    atr = data['ATR'].iloc[current_idx]
    take_profit_level = entry_price * (1 + 1 * atr)  # 1.5 times
    stop_loss_level = entry_price - 1 * atr  # 1.0 times


    if current_close >= take_profit_level:
        return True, take_profit_level, 'ATR stop winning'
    elif current_close <= stop_loss_level:
        return True, stop_loss_level, 'stop loss'
    elif data['Exit_Signal'].iloc[current_idx]:
        return True, current_close, 'exit signal'
    else:
        return False, None, None


symbol = 'AAPL'
stock = yf.Ticker(symbol)
data = stock.history(period=f"{1}y")[['Close','High',"Low"]]  # Fetch data and select 'Close' column
data = data.reset_index()  # Reset index to include 'Date' as a column
data["Date"] = pd.to_datetime(data.Date)
print(data.head())

# calculate the indicator
data['RSI'] = calculate_rsi(data)
data['EMA_Fast'] = calculate_ema(data, 5)
data['EMA_Slow'] = calculate_ema(data, 13)
data['PLR_Slope'] = calculate_plr_slope(data, 5)

# plr rate
data['Prev_PLR_Slope'] = data['PLR_Slope'].shift(5)  # step 5
data['PLR_Slope_Increase'] = (data['PLR_Slope'] > 0)
#data['PLR_Slope_Increase'] = (data['PLR_Slope'] > 0) & (data['PLR_Slope'] > data['Prev_PLR_Slope'])

# generate the signal

data['EMA_Condition'] = (data['Close'] > data['EMA_Fast']) & (data['Close'] > data['EMA_Slow']) & (
            data['EMA_Fast'] > data['EMA_Slow'])
data['Near_EMA_Slow'] = (data['Close'] <= data['EMA_Slow'] * 1.02) & (data['Close'] >= data['EMA_Slow'] * 0.98)  # ±2%

#ATR
data['ATR'] = calculate_atr(data)
# buy signal
data['Entry_Signal'] = (
        (data['RSI'] < 70) &  # RSI
        data['PLR_Slope_Increase'] &
        data['EMA_Condition'] &
        data['Near_EMA_Slow']
)

# sell signal
data['EMA_Death_Cross'] = (data['EMA_Fast'] < data['EMA_Slow']) & (data['EMA_Fast'].shift(1) >= data['EMA_Slow'].shift(1))
data['Exit_Signal'] = (
        (data['RSI'] > 30) &  # RSI
        ((data['Close'] < data['EMA_Fast']) | data['EMA_Death_Cross']) &
        (data['PLR_Slope'] < 0)
)

# simulation
trades = []
position = False
entry_price = 0
entry_index = 0

for i in range(len(data)):
    # buy logic
    if not position and data['Entry_Signal'].iloc[i]:
        position = True
        entry_price = data['Close'].iloc[i]
        entry_index = i
        trades.append({'Action': 'Buy', 'Price': entry_price, 'Date': data.index[i]})

    # sell logic
    elif position:
        should_exit, exit_price, exit_reason = dynamic_exit_rule(data, entry_index, i, entry_price)

        if should_exit:
            position = False
            pct = (exit_price - entry_price) / entry_price * 100
            trades.append({
                'Action': 'Sell',
                'Price': exit_price,
                'Pct_Change': pct,
                'Date': data.index[i],
                'Reason': exit_reason
            })


# trade log
print("trade log:")
for trade in trades:
    print(f"{trade['Date']} {trade['Action']} @ {trade['Price']:.2f}", end="")
    if 'Pct_Change' in trade:
        print(f" ({trade['Pct_Change']:.2f}%) - {trade['Reason']}")


# performance
sell_trades = [t for t in trades if t['Action'] == 'Sell']

if sell_trades:
    win_rate = len([t for t in sell_trades if t['Pct_Change'] > 0]) / len(sell_trades)
    avg_return = sum(t['Pct_Change'] for t in sell_trades) / len(sell_trades)

    print(f"""
    === Report of the trade condition ===
    Total Trades: {len(sell_trades)}
    winning rate: {win_rate * 100:.2f}%
    average return: {avg_return:.2f}%
    Max signal win: {max(t['Pct_Change'] for t in sell_trades):.2f}%
    Max signal loss: {min(t['Pct_Change'] for t in sell_trades):.2f}%
    """)
