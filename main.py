import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from indicator import TrendStrategy

#
class TradingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("quint v1.0")
        self.setup_ui()
        self.strategy = None

    def setup_ui(self):
        # control frame
        control_frame = ttk.LabelFrame(self.root, text="parameter setting", padding=10)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="stock ttk").grid(row=0, column=0)
        self.symbol_entry = ttk.Entry(control_frame)
        self.symbol_entry.insert(0, "AAPL")
        self.symbol_entry.grid(row=0, column=1)

        ttk.Label(control_frame, text="time zone").grid(row=1, column=0)
        self.period_combo = ttk.Combobox(control_frame,
                                         values=['1mo', '3mo', '6mo', '1y', '2y', '5y'])
        self.period_combo.current(3)
        self.period_combo.grid(row=1, column=1)

        ttk.Button(control_frame, text="run strategy",
                   command=self.run_strategy).grid(row=2, columnspan=2, pady=10)

        # 结果显示
        result_frame = ttk.LabelFrame(self.root, text="result", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.result_text = tk.Text(result_frame, height=8)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # 图表区域
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=result_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def run_strategy(self):
        symbol = self.symbol_entry.get()
        period = self.period_combo.get()

        self.strategy = TrendStrategy(symbol=symbol, period=period)
        data = self.strategy.run()

        self.display_results(data)
        self.plot_data(data)

    def display_results(self, data):
        self.result_text.delete(1.0, tk.END)
        last_signal = data['Buy_Signal'].iloc[-1]
        self.result_text.insert(tk.END,
                                f"new_signal: {'buy' if last_signal == 1 else 'observe'}\n\n")
        self.result_text.insert(tk.END, data.tail().to_string())

    def plot_data(self, data):
        self.ax.clear()
        data['Close'].plot(ax=self.ax, label='Price', color='blue')
        data['EMA_Fast'].plot(ax=self.ax, label='EMA_Fast', color='orange')
        data['EMA_Slow'].plot(ax=self.ax, label='EMA_Slow', color='green')

        buy_signals = data[data['Buy_Signal'] == 1]
        self.ax.scatter(buy_signals.index, buy_signals['Close'],
                        color='red', marker='^', label='buy_signal')

        self.ax.legend()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = TradingGUI(root)
    root.geometry("800x600")
    root.mainloop()