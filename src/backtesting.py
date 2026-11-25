"""Educational moving-average crossover backtest with basic trading costs."""
import pandas as pd


def run_sma_crossover_backtest(df: pd.DataFrame, fast_window=20, slow_window=50,
                               fee_bps=5.0) -> tuple[pd.DataFrame, dict]:
    """
    Long/cash strategy:
    - Enter when fast SMA is above slow SMA.
    - Exit/hold cash otherwise.
    - Shift the position by one bar so today's close-derived signal is not
      applied to the same day's return (basic look-ahead-bias protection).
    fee_bps is the assumed one-way transaction cost in basis points.
    """
    if fast_window >= slow_window:
        raise ValueError("fast_window must be smaller than slow_window.")
    result = df.copy()
    fast = result["Close"].rolling(fast_window).mean()
    slow = result["Close"].rolling(slow_window).mean()
    signal = (fast > slow).astype(float)
    position = signal.shift(1).fillna(0.0)
    turnover = position.diff().abs()
    if len(turnover):
        turnover.iloc[0] = abs(position.iloc[0])
    cost_rate = fee_bps / 10000.0
    result["Strategy_Position"] = position
    result["Strategy_Turnover"] = turnover
    result["Strategy_Return"] = (
        position * result["Close"].pct_change().fillna(0.0)
        - turnover * cost_rate
    )
    result["Buy_Hold_Return"] = result["Close"].pct_change().fillna(0.0)
    result["Strategy_Equity"] = (1 + result["Strategy_Return"]).cumprod()
    result["Buy_Hold_Equity"] = (1 + result["Buy_Hold_Return"]).cumprod()

    strategy_total = float(result["Strategy_Equity"].iloc[-1] - 1)
    buy_hold_total = float(result["Buy_Hold_Equity"].iloc[-1] - 1)
    daily = result["Strategy_Return"]
    annual_vol = float(daily.std() * (252 ** 0.5)) if len(daily) > 1 else float("nan")
    metrics = {
        "fast_window": fast_window,
        "slow_window": slow_window,
        "fee_bps_one_way": fee_bps,
        "strategy_return_pct": strategy_total * 100,
        "buy_hold_return_pct": buy_hold_total * 100,
        "strategy_annualized_volatility_pct": annual_vol * 100,
        "number_of_position_changes": int((turnover > 0).sum()),
    }
    return result, metrics
