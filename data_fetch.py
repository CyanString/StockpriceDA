import yfinance as yf
import pandas as pd
import os


def fetch_stock_data(stock_name, period):
    """
    Fetches historical stock data for the given stock name and period.

    Args:
        stock_name (str): The stock ticker symbol (e.g., "AAPL").
        period (int): The number of years of data to fetch.

    Returns:
        pd.DataFrame: A DataFrame containing the historical stock data.
    """
    try:
        stock = yf.Ticker(stock_name)
        history = stock.history(period=f"{period}y")[['Close']]  # Fetch data and select 'Close' column
        history = history.reset_index()  # Reset index to include 'Date' as a column
        history["Date"] = pd.to_datetime(history.Date)
        return history
    except Exception as e:
        print(f"Error fetching data for {stock_name}: {e}")
        return None


def save_to_csv(data, file_name):
    """
    Saves the DataFrame to a CSV file if the file does not already exist.

    Args:
        data (pd.DataFrame): The DataFrame to save.
        file_name (str): The name of the CSV file.
    """
    if file_name in os.listdir():
        print(f"File '{file_name}' already exists. ")
        return

    file_path = os.path.join(os.getcwd(), file_name)
    try:
        data.to_csv(file_path, index=False)
        print(f"Data saved successfully at: {file_path}")
    except Exception as e:
        print(f"Error saving data to {file_name}: {e}")

