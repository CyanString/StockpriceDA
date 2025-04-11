import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from indicator import TrendStrategy
import numpy as np

#1
class TradingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quint Strategy Model")
        self.setup_ui()
        self.strategy = None

    def setup_ui(self):
        # control frame
        control_frame = ttk.LabelFrame(self.root, text="parameter setting", padding=10)
        control_frame.pack(fill=tk.X, padx=5, pady=5)


        ttk.Label(control_frame, text="Stock token:").grid(row=0, column=0)
        self.symbol_combo = ttk.Combobox(control_frame,
                                          values=["AAPL","MSFT","NVDA","GOOGL","AMZN",
                                                  "META","TSLA","AVGO","ASML","ADBE"])
        self.symbol_combo.current(0)
        self.symbol_combo.grid(row=0, column=1)


        ttk.Label(control_frame, text="time zone").grid(row=1, column=0)
        self.period_combo = ttk.Combobox(control_frame,
                                         values=['1mo', '3mo', '6mo', '1y', '2y', '5y'])
        self.period_combo.current(3)
        self.period_combo.grid(row=1, column=1)

        ttk.Button(control_frame, text="run strategy",
                   command=self.run_strategy).grid(row=2, columnspan=2, pady=10)

        # result report
        result_frame = ttk.LabelFrame(self.root, text="result", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.result_text = tk.Text(result_frame, height=8)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # graph region
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=result_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        ttk.Label(control_frame, text="TP Multiplier").grid(row=3, column=0)
        self.tp_entry = ttk.Entry(control_frame)
        self.tp_entry.insert(0, "1.5")
        self.tp_entry.grid(row=3, column=1)

        ttk.Label(control_frame, text="SL Multiplier").grid(row=4, column=0)
        self.sl_entry = ttk.Entry(control_frame)
        self.sl_entry.insert(0, "0.8")
        self.sl_entry.grid(row=4, column=1)




    def run_strategy(self):


        symbol = self.symbol_combo.get()
        period = self.period_combo.get()

        try:
            tp = float(self.tp_entry.get())
            sl = float(self.sl_entry.get())
        except ValueError:
            self.result_text.insert(tk.END, "Error: TP/SL must be numbers!")
            return

        self.strategy = TrendStrategy(symbol=symbol, period=period,tp_multiplier=tp, sl_multiplier=sl)
        data = self.strategy.run()
        trades, stats = self.strategy.run_backtest(data)

        filename = symbol + "-" + period + ".csv"
        self.strategy.save_to_csv(data,filename)

        self.display_results(data, stats)
        self.plot_data(data,trades)

    def display_results(self, data, stats):
        self.result_text.delete(1.0, tk.END)
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



if __name__ == "__main__":
    root = tk.Tk()
    app = TradingGUI(root)
    root.geometry("800x600")
    root.mainloop()