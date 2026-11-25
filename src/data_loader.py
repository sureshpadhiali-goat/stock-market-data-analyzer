from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_CSV = PROJECT_ROOT / "data" / "sample_stock_data.csv"


def load_from_yfinance(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download daily historical prices. The end date is exclusive in yfinance."""
    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError("yfinance is not installed. Run: pip install -r requirements.txt") from exc
    raw = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    if raw.empty:
        raise ValueError(f"No market data returned for {ticker}. Check ticker, dates, or internet access.")

    # yfinance may return either ordinary columns or a MultiIndex, depending on version/ticker.
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    raw = raw.reset_index()
    if "Date" not in raw.columns:
        raw = raw.rename(columns={raw.columns[0]: "Date"})
    return raw


def load_from_csv(csv_path: str | None = None) -> pd.DataFrame:
    """Load local data. CSV must contain a Date column and at least Close."""
    path = Path(csv_path) if csv_path else SAMPLE_CSV
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    return pd.read_csv(path)


def get_market_data(ticker: str, start: str, end: str,
                    source: str = "auto", csv_path: str | None = None) -> tuple[pd.DataFrame, str]:
    """Return (data, source label). auto falls back to the bundled demonstration CSV."""
    if source in ("auto", "yfinance"):
        try:
            return load_from_yfinance(ticker, start, end), "Yahoo Finance"
        except Exception as exc:
            if source == "yfinance":
                raise
            print(f"[INFO] Online download unavailable: {exc}")
            print("[INFO] Falling back to bundled sample dataset.")
    return load_from_csv(csv_path), "Local CSV / sample data"
