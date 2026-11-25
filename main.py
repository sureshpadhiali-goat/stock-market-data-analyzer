from datetime import date
import argparse

from src.analyzer import run_analysis


def parse_args():
    parser = argparse.ArgumentParser(description="Stock Market Data Analyzer")
    parser.add_argument("--ticker", default="RELIANCE.NS", help="Yahoo Finance ticker, e.g. RELIANCE.NS or AAPL")
    parser.add_argument("--start", default="2024-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", default=date.today().isoformat(), help="End date YYYY-MM-DD (exclusive for yfinance)")
    parser.add_argument("--csv", default=None, help="Optional local CSV file with Date and Close columns")
    parser.add_argument("--source", choices=["auto", "yfinance", "csv"], default="auto",
                        help="auto tries Yahoo Finance then sample CSV; csv uses the supplied CSV or sample")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_analysis(
        ticker=args.ticker,
        start=args.start,
        end=args.end,
        csv_path=args.csv,
        source=args.source,
    )
