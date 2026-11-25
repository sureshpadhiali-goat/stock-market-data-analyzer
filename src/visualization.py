from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


def create_charts(df, ticker: str, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme()
    paths = []

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["Close"], label="Closing price", linewidth=1.6)
    ax.set(title=f"{ticker} — Closing Price", xlabel="Date", ylabel="Price")
    ax.legend()
    fig.tight_layout()
    path = output_dir / "closing_price.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    paths.append(path)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["Close"], label="Close", alpha=0.65)
    ax.plot(df.index, df["SMA_20"], label="20-day SMA")
    ax.plot(df.index, df["SMA_50"], label="50-day SMA")
    ax.set(title=f"{ticker} — Moving Averages", xlabel="Date", ylabel="Price")
    ax.legend()
    fig.tight_layout()
    path = output_dir / "moving_averages.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    paths.append(path)

    returns = df["Daily_Return"].dropna()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(returns, bins=35, edgecolor="black", alpha=0.75)
    ax.set(title=f"{ticker} — Daily Return Distribution", xlabel="Daily return", ylabel="Frequency")
    fig.tight_layout()
    path = output_dir / "daily_returns.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    paths.append(path)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df["Annualized_Volatility_20D"] * 100, label="20-day rolling annualized volatility")
    ax.set(title=f"{ticker} — Rolling Volatility", xlabel="Date", ylabel="Volatility (%)")
    ax.legend()
    fig.tight_layout()
    path = output_dir / "volatility.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    paths.append(path)
    return paths
