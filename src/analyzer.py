from pathlib import Path
import pandas as pd

from src.data_loader import get_market_data
from src.processing import clean_market_data, add_features, calculate_summary
from src.visualization import create_charts
from src.reporting import write_report


ROOT = Path(__file__).resolve().parents[1]


def run_analysis(ticker="RELIANCE.NS", start="2024-01-01", end="2025-01-01",
                 csv_path=None, source="auto"):
    print("=" * 62)
    print("STOCK MARKET DATA ANALYZER")
    print("=" * 62)
    raw, source_label = get_market_data(ticker, start, end, source, csv_path)
    print(f"[1/5] Data loaded from: {source_label} ({len(raw)} rows)")

    clean = clean_market_data(raw)
    print(f"[2/5] Cleaned dataset: {len(clean)} valid observations")

    featured = add_features(clean)
    print("[3/5] Calculated returns, SMA20, SMA50 and rolling volatility")

    output_dir = ROOT / "outputs"
    report_dir = ROOT / "reports"
    output_dir.mkdir(exist_ok=True)
    featured.to_csv(output_dir / "analyzed_stock_data.csv")
    summary = calculate_summary(featured, ticker, source_label)

    charts = create_charts(featured, ticker, output_dir)
    print(f"[4/5] Saved {len(charts)} charts in outputs/")

    report_path = write_report(summary, report_dir / "analysis_report.md")
    print("[5/5] Report generated")
    print("\n--- ANALYSIS SUMMARY ---")
    print(f"Ticker: {summary['ticker']}")
    print(f"Period: {summary['start_date']} to {summary['end_date']}")
    print(f"Latest close: {summary['latest_close']:.2f}")
    print(f"Period return: {summary['total_return_pct']:.2f}%")
    print(f"Annualized historical volatility: {summary['annualized_volatility_pct']:.2f}%")
    print(f"Trend: {summary['trend']}")
    print(f"Report: {report_path.relative_to(ROOT)}")
    print("Charts and processed CSV: outputs/")
    print("\nEducational analysis only — not financial advice.")
    return featured, summary
