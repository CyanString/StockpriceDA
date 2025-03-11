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


def main():
    """
    Main function to interact with the user and fetch/save stock data.
    """
    # Get user input
    stock_name = input("Enter the stock ticker symbol (e.g., AAPL): ").strip().upper()
    period = input("Enter the number of years of data to collect (e.g., 2): ").strip()

    # Validate period input
    try:
        period = int(period)
        if period <= 0:
            print("Please enter a valid positive integer for the period.")
            return
    except ValueError:
        print("Invalid input for period. Please enter a valid integer.")
        return

    # Fetch stock data
    print(f"Fetching {period} year(s) of data for {stock_name}...")
    stock_data = fetch_stock_data(stock_name, period)

    if stock_data is not None:
        # Generate file name
        file_name = f"{stock_name}_{period}_years_data.csv"

        # Save data to CSV
        save_to_csv(stock_data, file_name)


if __name__ == "__main__":
    main()