# Architecture

```text
Ticker + date range + source (Yahoo Finance / CSV)
                    |
                    v
             Data ingestion
                    |
                    v
       Validation and data cleaning
                    |
                    v
       Feature engineering (Pandas)
       - daily returns
       - SMA 20 / SMA 50
       - rolling volatility
       - cumulative returns
                    |
          +---------+---------+
          |                   |
          v                   v
    Visualizations       Summary metrics
          |                   |
          +---------+---------+
                    |
                    v
       CSV + Markdown + JSON reports
                    |
          Optional Streamlit UI
          Future FastAPI + Next.js
```

## Data flow
1. User supplies ticker, date range and source.
2. The loader downloads data or reads a local CSV.
3. The cleaning layer standardizes dates/numbers, removes invalid rows and sorts chronologically.
4. The processing layer calculates features with vectorized Pandas operations.
5. The analyzer calculates period-level metrics.
6. The visualization and reporting layers save reusable artifacts.

## Important design notes
- Yahoo Finance data is a convenient public source, not a guaranteed production feed or exchange-authoritative service.
- `yfinance` is an unofficial interface and may change or be rate-limited.
- For production systems, use a licensed, reliable market-data provider and review redistribution rights.
- Daily historical data is not live tick data. This starter project does not claim real-time execution capability.

## Backtesting extension
The optional SMA crossover example compares a long/cash rule with buy-and-hold. It shifts close-derived signals by one observation and applies a configurable one-way fee. It is deliberately simplified: no dividends, taxes, bid/ask spread, market impact, partial fills, shorting, corporate-action edge cases or walk-forward validation.
