# Stock Market Data Analyzer

A beginner-friendly, modular Python project for analyzing historical stock market data. It downloads daily prices using `yfinance` (when available) or loads a local CSV, cleans the data, calculates returns and moving averages, measures historical volatility, creates visualizations, and generates Markdown/JSON reports.

> **Disclaimer:** This project is for educational purposes only. It is not financial advice, an investment recommendation, or a production trading system. Historical performance does not guarantee future results.

## Problem statement
Raw market prices are difficult to interpret without cleaning, trend summaries, performance calculations and risk context. This project demonstrates a reproducible workflow that converts historical price data into structured analytical outputs.

## Industry relevance
The workflow reflects foundational tasks in financial analytics and FinTech data products: ingestion, validation, time-series feature engineering, visualization, reporting and (in future extensions) APIs and backtesting. It is a learning prototype, not a broker-grade market-data platform.

## Features
- Yahoo Finance historical data download using `yfinance`
- Local CSV fallback for offline/reproducible runs
- Date parsing, numeric conversion, duplicate removal and invalid-price filtering
- Daily simple returns and cumulative returns
- 20-observation and 50-observation simple moving averages
- 20-observation rolling and annualized historical volatility
- Highest/lowest closing-price analysis
- Closing-price, moving-average, daily-return and volatility charts
- Processed CSV, Markdown report and JSON summary
- Optional Streamlit dashboard

## Tech stack
Python, Pandas, NumPy, yfinance, Matplotlib, Seaborn, Streamlit (optional), Plotly (optional).

## Folder structure
```text
Stock-Market-Data-Analyzer/
├── data/                 # Bundled demonstration CSV
├── notebooks/            # Add exploratory notebooks here
├── src/                  # Reusable Python modules
│   ├── data_loader.py
│   ├── processing.py
│   ├── visualization.py
│   ├── reporting.py
│   └── analyzer.py
├── outputs/               # Generated CSV and charts
├── images/                # Curated screenshots for README
├── reports/               # Generated Markdown and JSON reports
├── docs/                  # Architecture, phases, screenshots, interview prep
├── main.py
├── app.py                 # Optional Streamlit dashboard
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

### Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the project

### Online data
```bash
python main.py --ticker RELIANCE.NS --start 2024-01-01 --end 2025-01-01 --source yfinance
```
The end date is exclusive in Yahoo Finance downloads.

### Automatic fallback
```bash
python main.py --ticker DEMO --source auto
```
This tries Yahoo Finance and uses `data/sample_stock_data.csv` if the download fails.

### CSV only
```bash
python main.py --source csv
```

### Your own CSV
Your CSV must contain `Date` and `Close` columns. Optional columns include `Open`, `High`, `Low` and `Volume`.
```bash
python main.py --source csv --csv data/my_stock.csv
```

### Optional dashboard
```bash
streamlit run app.py
```

## Generated outputs
- `outputs/analyzed_stock_data.csv` — source prices plus calculated features
- `outputs/closing_price.png` — closing price history
- `outputs/moving_averages.png` — close, SMA20 and SMA50
- `outputs/daily_returns.png` — distribution of daily returns
- `outputs/volatility.png` — rolling annualized volatility
- `reports/analysis_report.md` — human-readable report
- `reports/analysis_report.json` — machine-readable summary

The bundled sample CSV is a fabricated, illustrative dataset for software testing; it is not actual Reliance or exchange market history. It is intentionally small for demonstration. It has fewer than 50 observations, so SMA50 will be empty for that sample. Use a longer dataset to see both moving averages.

## Sample interpretation
The report describes the observed period return, highest and lowest closing prices, annualized historical volatility and the latest moving-average alignment. These are descriptive statistics, not forecasts or buy/sell recommendations.

## Screenshots
After running the application, copy selected charts from `outputs/` into `images/` and add them here:
```markdown
![Closing price](images/closing_price.png)
![Moving averages](images/moving_averages.png)
![Daily returns](images/daily_returns.png)
```

## Learning outcomes
- Python project structure and virtual environments
- Data ingestion from an API and CSV files
- Data cleaning and validation with Pandas
- Time-series indexing and rolling calculations
- Return and volatility calculations
- Data visualization and report generation
- Git/GitHub workflow and project documentation

## Roadmap
- Add unit tests and data-quality test cases
- Add benchmark comparison and configurable indicators
- Add a backtesting engine with transaction costs, slippage and no-lookahead safeguards
- Add FastAPI endpoints
- Add database persistence and scheduled refresh
- Add a Next.js dashboard and alerting

## Data-source note
`yfinance` is an unofficial open-source interface to Yahoo Finance. Availability, fields and rate limits can change. Check the relevant provider's terms and licensing before using data in a commercial or production application. This starter project uses daily historical prices; it does not provide guaranteed real-time market data.

## License
Choose a license before publishing. For a public learning repository, the MIT License is a common option; ensure any bundled data and third-party assets permit redistribution.
