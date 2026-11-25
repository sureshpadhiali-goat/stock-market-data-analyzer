"""Optional FastAPI service. Start with: uvicorn api:app --reload"""
from datetime import date, timedelta
from fastapi import FastAPI, HTTPException, Query

from src.data_loader import get_market_data
from src.processing import clean_market_data, add_features, calculate_summary
from src.backtesting import run_sma_crossover_backtest

app = FastAPI(title="Stock Market Data Analyzer API", version="1.0.0",
              description="Educational historical market data analytics API.")


@app.get("/health")
def health():
    return {"status": "ok", "service": "stock-market-data-analyzer"}


@app.get("/analyze")
def analyze(
    ticker: str = Query("RELIANCE.NS", min_length=1),
    start: date = Query(date.today() - timedelta(days=365)),
    end: date = Query(date.today()),
):
    if start >= end:
        raise HTTPException(status_code=400, detail="start must be earlier than end")
    try:
        raw, source = get_market_data(ticker.upper(), start.isoformat(), end.isoformat(), "yfinance")
        df = add_features(clean_market_data(raw))
        summary = calculate_summary(df, ticker.upper(), source)
        return {"summary": summary, "latest_observations": df.tail(10).reset_index().to_dict(orient="records")}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Unable to analyze requested data: {exc}") from exc


@app.get("/backtest")
def backtest(
    ticker: str = Query("RELIANCE.NS", min_length=1),
    start: date = Query(date.today() - timedelta(days=730)),
    end: date = Query(date.today()),
    fast_window: int = Query(20, ge=2, le=200),
    slow_window: int = Query(50, ge=3, le=500),
    fee_bps: float = Query(5.0, ge=0, le=500),
):
    if start >= end:
        raise HTTPException(status_code=400, detail="start must be earlier than end")
    if fast_window >= slow_window:
        raise HTTPException(status_code=400, detail="fast_window must be smaller than slow_window")
    try:
        raw, _ = get_market_data(ticker.upper(), start.isoformat(), end.isoformat(), "yfinance")
        df = add_features(clean_market_data(raw))
        _, metrics = run_sma_crossover_backtest(df, fast_window, slow_window, fee_bps)
        return {"ticker": ticker.upper(), "metrics": metrics,
                "note": "Illustrative backtest only; excludes taxes, market impact, liquidity constraints and other real-world frictions."}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Backtest failed: {exc}") from exc
