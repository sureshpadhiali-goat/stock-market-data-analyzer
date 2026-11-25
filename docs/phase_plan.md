# Phase-wise implementation plan

| Phase | Work | Why | Expected output | Common mistake |
|---|---|---|---|---|
| 1 Setup | Install Python, VS Code, Git | Reproducible environment | Working Python terminal | Multiple Python installations |
| 2 Structure | Create folders and modules | Maintainable code | Project skeleton | Putting everything in one file |
| 3 Data collection | yfinance + CSV fallback | Obtain testable data | Raw prices | Wrong ticker/date format |
| 4 Cleaning | Parse dates, numeric columns, duplicates | Reliable calculations | Clean time series | Treating missing values as zero |
| 5 EDA | Inspect rows, ranges, summary statistics | Understand data quality | Dataset profile | Assuming every trading day exists |
| 6 Moving averages | SMA20 and SMA50 | Smooth short/medium trends | Indicator columns | Interpreting lagging indicators as forecasts |
| 7 Returns/risk | Daily returns and volatility | Measure historical performance/risk | Metrics | Comparing volatility without same time basis |
| 8 Visualization | Price, SMA, returns, volatility charts | Communicate patterns | PNG charts | Misleading axes or unlabeled units |
| 9 Reporting | Markdown and JSON summary | Reproducibility | Report files | Calling historical metrics predictions |
| 10 GitHub | Commit code, docs, sample output | Proof of work | Public repository | Committing secrets or huge generated files |

## Suggested six-day proof plan
- Day 1: environment, folders, requirements, README skeleton. Commit: `chore: initialize project structure`.
- Day 2: data loader and sample CSV fallback. Commit: `feat: add Yahoo Finance and CSV data ingestion`.
- Day 3: cleaning and EDA checks. Commit: `feat: clean and validate historical price data`.
- Day 4: returns, SMA20/SMA50 and volatility. Commit: `feat: calculate returns moving averages and volatility`.
- Day 5: charts and dashboard basics. Commit: `feat: add price trend and risk visualizations`.
- Day 6: reports, documentation, screenshots and GitHub push. Commit: `docs: add analysis report and project documentation`.

Do not fake screenshots or claim live data if you used the sample CSV. Label sample runs clearly.
