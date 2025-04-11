# StockpriceDA project
## Overview
   This project implements a technical analysis-based trading strategy tool designed
   for return-seeking investors. The tool combines multiple technical indicators to
   identify potential trading opportunities and dynamically manage positions.
## Features
### Technical Indicators:

1. **EMA (Exponential Moving Average):** Identifies potential buy/sell points and market trends

2. **RSI (Relative Strength Index):** Detects overbought/oversold market conditions

3. **PLR (Piecewise Linear Regression):** Determines the overall trend direction

### Dynamic Exit Rule:

**ATR (Average True Range):** Implements dynamic profit-taking and stop-loss mechanisms

### Optimization:

Backtesting on historical data to find optimal parameter combinations (grid search)

Winning rate analysis for strategy validation

### User Interface:

1. Tkinter-based GUI for easy interaction

2. Stock and period selection

3. Performance visualization

4. Data export capabilities

## Useage
1. Run the application

2. Select your desired stock and time period

3. View the strategy performance metrics

4. Adjust parameters as needed (via code)

5. Save results for further analysis

##  Requirements

### General
- Install **Python** > 3.6.

### Python Packages
To run the project, you need to install the following Python libraries:

- **Pandas**: Data manipulation and CSV file handling.
- **Numpy**: Basic function.
- **Matplotlib**: Data visualizations.
- **yfinance**: Sourse of the data
- **tkinter**: Interface generator

---

## User Interface


![Stock Price Plot](stock_price_plots.png)







---

