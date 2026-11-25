from pathlib import Path
import json
import math


def _fmt(value, suffix=""):
    if value is None:
        return "N/A"
    try:
        if math.isnan(float(value)):
            return "N/A"
    except (TypeError, ValueError):
        pass
    return f"{value:,.2f}{suffix}"


def write_report(summary: dict, report_path: Path) -> Path:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Stock Analysis Report: {summary['ticker']}",
        "",
        f"- Data source: {summary['source']}",
        f"- Period: {summary['start_date']} to {summary['end_date']}",
        f"- Observations: {summary['observations']}",
        "",
        "## Price summary",
        f"- First close: {_fmt(summary['first_close'])}",
        f"- Latest close: {_fmt(summary['latest_close'])}",
        f"- Highest close: {_fmt(summary['highest_close'])} on {summary['highest_close_date']}",
        f"- Lowest close: {_fmt(summary['lowest_close'])} on {summary['lowest_close_date']}",
        "",
        "## Performance and risk",
        f"- Period return: {_fmt(summary['total_return_pct'], '%')}",
        f"- Average daily return: {_fmt(summary['average_daily_return_pct'], '%')}",
        f"- Annualized historical volatility: {_fmt(summary['annualized_volatility_pct'], '%')}",
        "",
        "## Trend observation",
        summary["trend"],
        "",
        "## Interpretation notes",
        "- Moving averages are lagging indicators; they summarize past prices.",
        "- Historical volatility measures dispersion of past daily returns, not the probability of loss.",
        "- Period return does not include transaction costs, taxes, dividends unless reflected in adjusted prices, or slippage.",
        "- This report is educational and is not financial advice.",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    json_path = report_path.with_suffix(".json")
    json_path.write_text(json.dumps(summary, indent=2, allow_nan=True), encoding="utf-8")
    return report_path
