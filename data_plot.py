import matplotlib.pyplot as plt
import pandas as pd
import os




DIR = 'stockprice_data/'
FILES_DATA = ['NVIDIA Stock Price History.csv', 'Meta Platforms Stock Price History.csv',
              'Microsoft Stock Price History.csv','Tesla Stock Price History.csv' ]

plot_data = []

for file in FILES_DATA:
   price= pd.read_csv(os.path.join(DIR,file))
   price['Date'] = pd.to_datetime(price['Date'])
   price = price.sort_values('Date')
   COMPANY_NAME = file.split(' ')[0]
   plot_data.append((COMPANY_NAME, price))

# plot all four graph
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes_pos = [(0, 0), (0, 1), (1, 0), (1, 1)]
color = ['red', 'blue', 'green', 'orange']

for idx,(COMPANY_NAME, price) in enumerate(plot_data):
    row, col = axes_pos[idx]
    ax = axes[row, col]
    ax.plot(price['Date'], price['Price'], label='Closed Price',color=color[idx])
    ax.set_title(f'{COMPANY_NAME} Stock Price 2024-2025')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.savefig('stock_price_plots.png')
plt.show()
