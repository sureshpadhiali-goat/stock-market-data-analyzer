import numpy as np
import pandas as pd


PRICE_CANDIDATES = ["Close", "Adj Close", "close", "adj_close", "Adj_Close"]


def clean_market_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Normalize columns, parse dates, remove invalid rows, sort and de-duplicate."""
    if raw is None or raw.empty:
        raise ValueError("Input dataset is empty.")

    df = raw.copy()
    df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]

    # Normalize common column names.
    rename = {}
    for col in df.columns:
        low = col.lower()
        if low == "date":
            rename[col] = "Date"
        elif low in ("adj_close", "adjclose"):
            rename[col] = "Adj_Close"
        elif low == "close":
            rename[col] = "Close"
        elif low == "open":
            rename[col] = "Open"
        elif low == "high":
            rename[col] = "High"
        elif low == "low":
            rename[col] = "Low"
        elif low in ("volume",):
            rename[col] = "Volume"
    df = df.rename(columns=rename)

    if "Date" not in df.columns:
        raise ValueError("CSV/data must contain a Date column.")
    if "Close" not in df.columns and "Adj_Close" in df.columns:
        df["Close"] = df["Adj_Close"]
    if "Close" not in df.columns:
        raise ValueError("CSV/data must contain Close or Adj Close.")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True).dt.tz_convert(None)
    numeric_cols = [c for c in ["Open", "High", "Low", "Close", "Adj_Close", "Volume"] if c in df.columns]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Date", "Close"])
    df = df[df["Close"] > 0]
    df = df.sort_values("Date").drop_duplicates(subset=["Date"], keep="last")
    df = df.set_index("Date")
    if df.empty:
        raise ValueError("No valid rows remain after cleaning.")
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add daily returns, simple moving averages and annualized historical volatility."""
    result = df.copy()
    result["Daily_Return"] = result["Close"].pct_change()
    result["SMA_20"] = result["Close"].rolling(window=20, min_periods=20).mean()
    result["SMA_50"] = result["Close"].rolling(window=50, min_periods=50).mean()
    result["Daily_Volatility_20D"] = result["Daily_Return"].rolling(20).std()
    result["Annualized_Volatility_20D"] = result["Daily_Volatility_20D"] * np.sqrt(252)
    result["Cumulative_Return"] = (1 + result["Daily_Return"].fillna(0)).cumprod() - 1
    return result


def calculate_summary(df: pd.DataFrame, ticker: str, source: str) -> dict:
    close = df["Close"].dropna()
    returns = df["Daily_Return"].dropna()
    if close.empty:
        raise ValueError("No closing prices available.")
    first_price, last_price = float(close.iloc[0]), float(close.iloc[-1])
    total_return = (last_price / first_price) - 1
    annual_vol = float(returns.std() * np.sqrt(252)) if len(returns) > 1 else float("nan")
    latest = df.iloc[-1]
    sma20 = latest.get("SMA_20", np.nan)
    sma50 = latest.get("SMA_50", np.nan)

    if pd.notna(sma20) and pd.notna(sma50):
        if latest["Close"] > sma20 > sma50:
            trend = "Positive alignment (price > SMA20 > SMA50)"
        elif latest["Close"] < sma20 < sma50:
            trend = "Negative alignment (price < SMA20 < SMA50)"
        else:
            trend = "Mixed / sideways alignment"
    else:
        trend = "Insufficient history for both moving averages"

    return {
        "ticker": ticker,
        "source": source,
        "observations": int(len(df)),
        "start_date": df.index.min().date().isoformat(),
        "end_date": df.index.max().date().isoformat(),
        "first_close": first_price,
        "latest_close": float(last_price),
        "highest_close": float(close.max()),
        "highest_close_date": close.idxmax().date().isoformat(),
        "lowest_close": float(close.min()),
        "lowest_close_date": close.idxmin().date().isoformat(),
        "total_return_pct": float(total_return * 100),
        "average_daily_return_pct": float(returns.mean() * 100) if len(returns) else float("nan"),
        "annualized_volatility_pct": float(annual_vol * 100),
        "trend": trend,
    }
