
import os
from indicator import generate_signals, signal_plot, calculate_return
import pandas as pd
import matplotlib.pyplot as plt


class TrendlineAnalysis:
    def __init__(self):
        self.data = None
        self.method = None

    def load_data(self, filepath):
        """Loads data from a CSV file and ensures the date column is properly formatted."""
        self.data = pd.read_csv(filepath)
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data.set_index('Date', inplace=True)

    def setMethod(self, method='EMA'):
        """Sets the trend detection method."""
        self.method = method
    def EMA(self):
        self.data['EMA'] = self.data['Close'].ewm(span=30, adjust=False).mean()

    def signals(self):
        """Uses the EMA method to detect trends."""
        self.data['Buy signal'],self.data['Sell signal'] = generate_signals(self.data)
        return 0

    def plot(self):
        signal_plot(self.data)

    def analysis(self):
        """Displays trend analysis results."""
        calculate_return(self.data)







