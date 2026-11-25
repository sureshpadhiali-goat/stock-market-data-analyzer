# Interview preparation

## 1. Explain your project.
**Answer:** I built a Python-based Stock Market Data Analyzer that collects historical stock prices from Yahoo Finance or a local CSV, validates and cleans the data, calculates daily returns, 20-day and 50-day simple moving averages, and rolling annualized volatility. It generates price, trend, return-distribution and volatility charts, plus CSV and Markdown/JSON reports. The focus is reproducible data analysis, not automated investment advice.

## 2. Why did you use Pandas?
Pandas provides labeled time-series data structures, date indexing, missing-value handling, rolling windows and vectorized calculations. It avoids writing slow row-by-row loops for common analytics.

## 3. What is a daily return?
Daily simple return is `(today_close / previous_close) - 1`. It expresses the percentage change between two consecutive observations. It is undefined for the first observation because there is no previous close.

## 4. What is a moving average?
A simple moving average is the arithmetic mean of closing prices over a fixed number of observations. SMA20 uses the latest 20 observations and SMA50 uses 50. It smooths short-term fluctuations but lags price changes.

## 5. What does volatility measure?
Historical volatility commonly uses the standard deviation of periodic returns. This project annualizes daily standard deviation by multiplying by the square root of 252, assuming roughly 252 trading sessions per year. It is a historical dispersion measure, not a loss forecast.

## 6. Why clean data before analysis?
Bad dates, duplicate records, missing prices or non-numeric values can distort returns and indicators. Cleaning makes the calculation process more reliable and repeatable.

## 7. Why include CSV fallback?
It makes the project reproducible when internet access, provider availability or rate limits prevent downloading data. It also allows testing with a known dataset.

## 8. What are the limitations?
Yahoo Finance is not a guaranteed production feed; data may be delayed, incomplete or changed. The starter version uses daily bars, simple indicators and no transaction costs, slippage or execution simulation. It is not a validated trading system.

## 9. How would you improve it?
Add unit tests, a licensed data provider, database storage, configurable indicators, a vectorized backtesting module with transaction costs, FastAPI endpoints, authentication, scheduled refresh and a dashboard.

## 10. How is this relevant to a Data Analyst role?
It demonstrates data ingestion, data quality checks, time-series transformations, feature engineering, statistical summaries, visualization, report generation and clear communication of findings.

## HR explanation (30 seconds)
I developed this project to apply Python to a real-world financial dataset. It takes historical stock prices, cleans them, calculates performance and risk indicators, and presents the results through charts and a report. It helped me practice end-to-end data analysis and writing modular, reusable Python code.

## Technical explanation (60 seconds)
The application is split into ingestion, cleaning, feature engineering, analysis, visualization and reporting modules. The loader supports Yahoo Finance and CSV input. Pandas handles date-indexed time-series data, returns and rolling indicators. NumPy is used for annualization, while Matplotlib and Seaborn create charts. Outputs include processed CSV data, a Markdown report and a JSON summary. A Streamlit interface is included as an optional presentation layer.

## Interview honesty
Only claim the components you have personally run and understood. The optional dashboard is an extension until you have executed it. Do not call daily historical data live data, and do not claim a backtesting engine exists in this starter version.
