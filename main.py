
import os
from indicator import generate_signals, signal_plot, calculate_return
import data_fetch
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

class TrendlineAnalysis:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Analysis")
        self.root.geometry("400x200")

        # Configure style
        self.style = ttk.Style()
        self.style.configure('Modern.TFrame', background='#f0f0f0')
        self.style.configure('Modern.TLabel', background='#f0f0f0', font=('Helvetica', 10))
        self.style.configure('Modern.TButton', font=('Helvetica', 10))

        self.create_widgets()

    def create_widgets(self):
        """Creates the GUI widgets for user input."""
        main_frame = ttk.Frame(self.root, padding="20", style='Modern.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        entry_width = 20

        # Stock Input
        ttk.Label(main_frame, text="Stock Ticker:", style='Modern.TLabel').grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.stock_entry = ttk.Entry(main_frame, width=entry_width)
        self.stock_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Period Input
        ttk.Label(main_frame, text="Period (years):", style='Modern.TLabel').grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.period_entry = ttk.Entry(main_frame, width=entry_width)
        self.period_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Method Selection
        ttk.Label(main_frame, text="Analysis Method:", style='Modern.TLabel').grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.method_var = tk.StringVar(value="EMA")
        self.method_menu = ttk.Combobox(main_frame, textvariable=self.method_var, values=["EMA", "RSI"], width=entry_width - 2)
        self.method_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Button to fetch results
        self.fetch_button = ttk.Button(main_frame, text="Run Result", command=self.run_analysis)
        self.fetch_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    def run_analysis(self):
        stock = self.stock_entry.get()
        period = self.period_entry.get()
        method = self.method_var.get()
        print(f"Running {method} analysis for {stock} over {period} years.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TrendlineAnalysis(root)
    root.mainloop()
