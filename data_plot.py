import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

DIR = 'stockprice_data/'
FILES_DATA = ['NVIDIA Stock Price History.csv', 'Meta Platforms Stock Price History.csv', ..]

for file in FILES_DATA:
   price= pd.read_csv(os.path.join(DIR,file))

# Read the csv file
nvidia_price = pd.read_csv('stockprice_data/NVIDIA Stock Price History.csv')
meta_price = pd.read_csv('stockprice_data/Meta Platforms Stock Price History.csv')
microsoft_price = pd.read_csv('stockprice_data/Microsoft Stock Price History.csv')
tesla_price = pd.read_csv('stockprice_data/Tesla Stock Price History.csv')

# change the Date to the  proper formate
nvidia_price['Date'] = pd.to_datetime(nvidia_price['Date'])
meta_price['Date'] = pd.to_datetime(meta_price['Date'])
microsoft_price['Date'] = pd.to_datetime(microsoft_price['Date'])
tesla_price['Date'] = pd.to_datetime(tesla_price['Date'])

#sort the date
nvidia_price = nvidia_price.sort_values('Date')
meta_price = meta_price.sort_values('Date')
microsoft_price = microsoft_price.sort_values('Date')
tesla_price = tesla_price.sort_values('Date')

# plot all four graph
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# NVIDIA
axes[0, 0].plot(nvidia_price['Date'], nvidia_price['Price'], label='Closed Price', color='blue')
axes[0, 0].set_title('NVIDIA Stock Price 2024-2025')
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Price (USD)')
axes[0, 0].legend()
axes[0, 0].grid(True)

# Meta
axes[0, 1].plot(meta_price['Date'], meta_price['Price'], label='Closed Price', color='green')
axes[0, 1].set_title('Meta Stock Price 2024-2025')
axes[0, 1].set_xlabel('Date')
axes[0, 1].set_ylabel('Price (USD)')
axes[0, 1].legend()
axes[0, 1].grid(True)

# Microsoft
axes[1, 0].plot(microsoft_price['Date'], microsoft_price['Price'], label='Closed Price', color='orange')
axes[1, 0].set_title('Microsoft Stock Price 2024-2025')
axes[1, 0].set_xlabel('Date')
axes[1, 0].set_ylabel('Price (USD)')
axes[1, 0].legend()
axes[1, 0].grid(True)

# Tesla
axes[1, 1].plot(tesla_price['Date'], tesla_price['Price'], label='Closed Price', color='red')
axes[1, 1].set_title('Tesla Stock Price 2024-2025')
axes[1, 1].set_xlabel('Date')
axes[1, 1].set_ylabel('Price (USD)')
axes[1, 1].legend()
axes[1, 1].grid(True)

plt.tight_layout()
plt.savefig('stock_price_plots.png')  # 可以自定义路径和文件名，例如 ''
plt.show()