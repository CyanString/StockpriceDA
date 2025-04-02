import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

#
class TrendStrategy:
    def __init__(self, symbol='AAPL', period='1y',
                 rsi_window=14, ema_short=5, ema_long=13,
                 atr_window=14, plr_window=5):
        self.symbol = symbol
        self.period = period
        self.params = {
            'rsi_window': rsi_window,
            'ema_short': ema_short,
            'ema_long': ema_long,
            'atr_window': atr_window,
            'plr_window': plr_window
        }

    def _calculate_rsi(self, data):
        delta = data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(self.params['rsi_window']).mean()
        avg_loss = loss.rolling(self.params['rsi_window']).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def _calculate_ema(self, data, window):
        return data['Close'].ewm(span=window, adjust=False).mean()

    def _calculate_plr_slope(self,data, window):
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

    def _calculate_atr(self, data):
        high, low, close = data['High'], data['Low'], data['Close']
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(self.params['atr_window']).mean()

    def _dynamic_exit_rule(self, data, entry_idx, current_idx, entry_price):
        current_close = data['Close'].iloc[current_idx]
        atr = data['ATR'].iloc[current_idx]

        #
        take_profit = entry_price * (1 + 1.5 * atr / entry_price)
        stop_loss = entry_price * (1 - 0.8 * atr / entry_price)

        if current_close >= take_profit:
            return True, take_profit, 'take_profit'
        elif current_close <= stop_loss:
            return True, stop_loss, 'stop_loss'
        elif data['Exit_Signal'].iloc[current_idx]:
            return True, current_close, 'exit_signal'
        return False, None, None

    def run(self):
        # download the data
        stock = yf.Ticker(self.symbol)
        data = stock.history(period=self.period)[['Close', 'High', "Low"]]  # Fetch data and select 'Close' column
        data = data.reset_index()  # Reset index to include 'Date' as a column
        data["Date"] = pd.to_datetime(data.Date)

        # calculate the indicator
        data['RSI'] = self._calculate_rsi(data)
        data['EMA_Fast'] = self._calculate_ema(data, self.params['ema_short'])
        data['EMA_Slow'] = self._calculate_ema(data, self.params['ema_long'])
        data['PLR_Slope'] = self._calculate_plr_slope(data, self.params['plr_window'])
        data['ATR'] = self._calculate_atr(data)


        # plr rate
        data['Prev_PLR_Slope'] = data['PLR_Slope'].shift(5)  # step 5
        data['PLR_Slope_Increase'] = (data['PLR_Slope'] > 0)

        # bay/sell signal
        data['EMA_Condition'] = (data['Close'] > data['EMA_Fast']) & (data['Close'] > data['EMA_Slow']) & (
                data['EMA_Fast'] > data['EMA_Slow'])
        data['Near_EMA_Slow'] = (data['Close'] <= data['EMA_Slow'] * 1.02) & (
                    data['Close'] >= data['EMA_Slow'] * 0.98)  # ±2%

        data['Buy_Signal'] = (
                (data['RSI'] < 70) &  # RSI
                data['PLR_Slope_Increase'] &
                data['EMA_Condition'] &
                data['Near_EMA_Slow']
        )

        data['Sell_Signal'] = (
            (data['RSI'] > 30) &
            ((data['Close'] < data['EMA_Fast']) | (data['EMA_Fast'] < data['EMA_Slow'])) &
            (data['PLR_Slope'] < 0)
        )

        return data


    def run_backtest(self):
        data = self.run
        #
        trades = []
        position = False
        entry_price = 0
        entry_index = 0

        for i in range(len(data)):
            if not position and data['Entry_Signal'].iloc[i]:
                position = True
                entry_price = data['Close'].iloc[i]
                entry_index = i
                trades.append({
                    'Action': 'Buy',
                    'Price': entry_price,
                    'Date': data.index[i],
                    'Shares': 100  #
                })

            elif position:
                should_exit, exit_price, exit_reason = self._dynamic_exit_rule(
                    data, entry_index, i, entry_price)

                if should_exit:
                    position = False
                    pct = (exit_price - entry_price) / entry_price * 100
                    trades.append({
                        'Action': 'Sell',
                        'Price': exit_price,
                        'Pct_Change': pct,
                        'Date': data.index[i],
                        'Reason': exit_reason,
                        'Shares': 100
                    })


        sell_trades = [t for t in trades if t['Action'] == 'Sell']
        stats = {
            'trades': trades,
            'total_trades': len(sell_trades),
            'win_rate': None,
            'avg_return': None,
            'max_win': None,
            'max_loss': None
        }

        if sell_trades:
            stats['win_rate'] = len([t for t in sell_trades if t['Pct_Change'] > 0]) / len(sell_trades)
            stats['avg_return'] = np.mean([t['Pct_Change'] for t in sell_trades])
            stats['max_win'] = max(t['Pct_Change'] for t in sell_trades)
            stats['max_loss'] = min(t['Pct_Change'] for t in sell_trades)

        return data, trades, stats


