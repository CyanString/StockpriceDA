import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from indicator import TrendStrategy
from itertools import product
import numpy as np

#1

class TradingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quint Strategy Model")
        self.setup_ui()
        self.best_params = None
        self.best_profit_factor = None
        self.strategy = None

    def setup_ui(self):
        # Configure style
        self.root.configure(bg='#f5f5f5')
        style = ttk.Style()
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 9))
        style.configure('TButton', font=('Segoe UI', 9, 'bold'), padding=5)
        style.configure('TCombobox', padding=3)
        style.configure('TEntry', padding=3)
        style.configure('TLabelFrame', font=('Segoe UI', 10, 'bold'), padding=10)

        # Main control frame with improved layout
        control_frame = ttk.LabelFrame(self.root, text="Strategy Parameters", padding=(15, 10))
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Stock selection - improved layout
        stock_frame = ttk.Frame(control_frame)
        stock_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky='ew')

        ttk.Label(stock_frame, text="Stock Symbol:").pack(side=tk.LEFT, padx=(0, 10))
        self.symbol_combo = ttk.Combobox(stock_frame,
                                         values=["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN",
                                                 "META", "TSLA", "AVGO", "ASML", "ADBE"],
                                         width=12)
        self.symbol_combo.current(0)
        self.symbol_combo.pack(side=tk.LEFT)

        # Time period - improved layout
        period_frame = ttk.Frame(control_frame)
        period_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky='ew')

        ttk.Label(period_frame, text="Time Period:").pack(side=tk.LEFT, padx=(0, 10))
        self.period_combo = ttk.Combobox(period_frame,
                                         values=['1mo', '3mo', '6mo', '1y', '2y', '5y'],
                                         width=12)
        self.period_combo.current(3)
        self.period_combo.pack(side=tk.LEFT)

        # Risk management section
        risk_frame = ttk.Frame(control_frame)
        risk_frame.grid(row=2, column=0, columnspan=2, pady=5)

        ttk.Label(risk_frame, text="TP Multiplier:").grid(row=0, column=0, padx=5, sticky='e')
        self.tp_entry = ttk.Entry(risk_frame, width=8)
        self.tp_entry.insert(0, "1.5")
        self.tp_entry.grid(row=0, column=1, sticky='w', pady=2)

        ttk.Label(risk_frame, text="SL Multiplier:").grid(row=1, column=0, padx=5, sticky='e')
        self.sl_entry = ttk.Entry(risk_frame, width=8)
        self.sl_entry.insert(0, "0.8")
        self.sl_entry.grid(row=1, column=1, sticky='w', pady=2)

        # Indicator parameters in a grid layout
        # Indicator parameters in a grid layout
        params = [
            ("RSI Window", "14", 'rsi_entry'),
            ("EMA Short", "5", 'ema_short_entry'),
            ("EMA Long", "13", 'ema_long_entry'),
            ("ATR Window", "14", 'atr_entry'),
            ("PLR Window", "5", 'plr_entry')
        ]

        # Create a frame inside control_frame for parameter layout
        param_frame = ttk.Frame(control_frame)
        param_frame.grid(row=3, column=0, columnspan=5, pady=5)

        for col, (label, default, attr_name) in enumerate(params):
            # Label
            ttk.Label(param_frame, text=label).grid(row=0, column=col, padx=5, pady=2, sticky='s')
            # Entry
            entry = ttk.Entry(param_frame, width=8, justify='center')
            entry.insert(0, default)
            entry.grid(row=1, column=col, padx=5, pady=2, sticky='n')
            setattr(self, attr_name, entry)

        # Action buttons with better styling
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)

        run_btn = ttk.Button(button_frame, text="Run Strategy",
                             command=self.run_strategy, width=15)
        run_btn.pack(side=tk.LEFT, padx=5)

        optimize_btn = ttk.Button(button_frame, text="Optimize",
                                  command=self.optimize_parameters, width=15)
        optimize_btn.pack(side=tk.LEFT, padx=5)

        # Result frame with improved layout
        result_frame = ttk.LabelFrame(self.root, text="Results", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Text results with scrollbar
        text_frame = ttk.Frame(result_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_text = tk.Text(text_frame, height=8, wrap=tk.WORD,
                                   yscrollcommand=scrollbar.set,
                                   padx=10, pady=10,
                                   font=('Consolas', 9))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_text.yview)

        # Graph area with improved styling
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.fig.patch.set_facecolor('#f5f5f5')
        self.ax.grid(True, linestyle='--', alpha=0.6)

        self.canvas = FigureCanvasTkAgg(self.fig, master=result_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=(10, 0))



    def run_strategy(self):


        symbol = self.symbol_combo.get()
        period = self.period_combo.get()

        try:
            params = {
            'rsi_window': int(self.rsi_entry.get()),
            'ema_short': int(self.ema_short_entry.get()),
            'ema_long': int(self.ema_long_entry.get()),
            'atr_window': int(self.atr_entry.get()),
            'plr_window': int(self.plr_entry.get()),
            'tp_multiplier': float(self.tp_entry.get()),
            'sl_multiplier': float(self.sl_entry.get())
            }

        except ValueError:
            self.result_text.insert(tk.END, "Error: TP/SL must be numbers!")
            return

        self.strategy = TrendStrategy(
            symbol=symbol,
            period=period,
            rsi_window=params['rsi_window'],
            ema_short=params['ema_short'],
            ema_long=params['ema_long'],
            atr_window=params['atr_window'],
            plr_window=params['plr_window'],
            tp_multiplier=params['tp_multiplier'],
            sl_multiplier=params['sl_multiplier']
        )

        data = self.strategy.run()
        trades, stats = self.strategy.run_backtest(data)

        filename = symbol + "-" + period + ".csv"
        self.strategy.save_to_csv(data,filename)

        self.display_results(data, stats)
        self.plot_data(data,trades)

    def display_results(self, data, stats):
        self.result_text.delete(1.0, tk.END)

        # Display results
        if self.best_params:
            self.result_text.insert(tk.END, "Optimization Results:\n\n")
            self.result_text.insert(tk.END, f"Best Parameters: {self.best_params}\n")
            self.result_text.insert(tk.END, f"Best Profit Factor: {self.best_profit_factor:.2f}\n\n")

        self.result_text.insert(tk.END,
                                f"Total Trades: {stats['total_trades']}\n"
                                f"Win Rate: {stats['win_rate'] * 100:.1f}%\n"
                                f"Avg Return: {stats['avg_return']:.2f}%\n"
                                f"Max Win: {stats['max_win']:.2f}%\n"
                                f"Max Loss: {stats['max_loss']:.2f}%\n"
                                )

    def plot_data(self, data,trades):
        self.ax.clear()
        data['Close'].plot(ax=self.ax, label='Price', color='blue')
        data['EMA_Fast'].plot(ax=self.ax, label='EMA_Fast', color='orange')
        data['EMA_Slow'].plot(ax=self.ax, label='EMA_Slow', color='green')

        buy_signals = data[data['Buy_Signal'] == 1]
        self.ax.scatter(buy_signals.index, buy_signals['Close'],
                        color='red', marker='^', label='buy_signal')

        sell_dates = [t['Date'] for t in trades if t['Action'] == 'Sell']
        sell_prices = [t['Price'] for t in trades if t['Action'] == 'Sell']
        self.ax.scatter(sell_dates, sell_prices,
                        color='black', marker='v', label='Sell Signal')

        self.ax.legend()
        self.canvas.draw()

    def optimize_parameters(self):
        symbol = self.symbol_combo.get()
        period = self.period_combo.get()

        # Define parameter ranges to test
        param_grid = {
            'rsi_window': [10, 14, 20],
            'ema_short': [3, 5, 8],
            'ema_long': [10, 13, 20],
            'plr_window': [3, 5, 8],
            'atr_window': [10, 14, 20],
            'tp_multiplier': [1.0, 1.5, 2.0],
            'sl_multiplier': [0.5, 0.8, 1.0]
        }

        best_params = None
        best_metric = -float('inf')
        results = []

        param_combinations = product(*param_grid.values())

        for params in param_combinations:
            current_params = dict(zip(param_grid.keys(), params))

            try:
                strategy = TrendStrategy(
                    symbol=symbol,
                    period=period,
                    **current_params
                )
                data = strategy.run()
                trades, stats = strategy.run_backtest(data)

                if stats['total_trades'] > 0:  # Only consider if we had trades
                    # Use profit factor as metric (can be changed to sharpe ratio, etc.)
                    wins = [t for t in trades if t['Action'] == 'Sell' and t['Pct_Change'] > 0]
                    losses = [t for t in trades if t['Action'] == 'Sell' and t['Pct_Change'] <= 0]

                    if len(losses) > 0:
                        profit_factor = sum(w['Pct_Change'] for w in wins) / abs(sum(l['Pct_Change'] for l in losses))
                    else:
                        profit_factor = float('inf')

                    results.append((current_params, profit_factor, stats))

                    if profit_factor > best_metric:
                        best_metric = profit_factor
                        best_params = current_params

            except Exception as e:
                print(f"Error with params {current_params}: {e}")

        # Display results
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Optimization Results:\n\n")
        self.result_text.insert(tk.END, f"Best Parameters: {best_params}\n")
        self.result_text.insert(tk.END, f"Best Profit Factor: {best_metric:.2f}\n\n")

        if best_params:
            self.best_params = best_params  # Store the best parameters as an instance variable
            self.best_profit_factor = best_metric
            self.update_parameter_fields(best_params)


    def update_parameter_fields(self, params):
        """Update all parameter fields with optimized values"""
        self.rsi_entry.delete(0, tk.END)
        self.rsi_entry.insert(0, str(params['rsi_window']))

        self.ema_short_entry.delete(0, tk.END)
        self.ema_short_entry.insert(0, str(params['ema_short']))

        self.ema_long_entry.delete(0, tk.END)
        self.ema_long_entry.insert(0, str(params['ema_long']))

        self.atr_entry.delete(0, tk.END)
        self.atr_entry.insert(0, str(params['atr_window']))

        self.plr_entry.delete(0, tk.END)
        self.plr_entry.insert(0, str(params['plr_window']))

        self.tp_entry.delete(0, tk.END)
        self.tp_entry.insert(0, str(params['tp_multiplier']))

        self.sl_entry.delete(0, tk.END)
        self.sl_entry.insert(0, str(params['sl_multiplier']))




if __name__ == "__main__":
    root = tk.Tk()
    app = TradingGUI(root)
    root.geometry("800x600")
    root.mainloop()