"""Optional Streamlit dashboard. Run: streamlit run app.py"""
from datetime import date, timedelta
import streamlit as st
import plotly.express as px

from src.data_loader import get_market_data
from src.processing import clean_market_data, add_features, calculate_summary

st.set_page_config(page_title="Stock Market Data Analyzer", layout="wide")
st.title("Stock Market Data Analyzer")
st.caption("Educational historical-market analysis — not investment advice.")

ticker = st.text_input("Yahoo Finance ticker", "RELIANCE.NS").strip().upper()
col1, col2 = st.columns(2)
start = col1.date_input("Start date", date.today() - timedelta(days=365))
end = col2.date_input("End date", date.today())
if st.button("Analyze", type="primary"):
    if start >= end:
        st.error("Start date must be earlier than end date.")
    else:
        with st.spinner("Loading and analyzing data..."):
            try:
                raw, source = get_market_data(ticker, start.isoformat(), end.isoformat(), "yfinance")
                df = add_features(clean_market_data(raw))
                summary = calculate_summary(df, ticker, source)
                a, b, c, d = st.columns(4)
                a.metric("Latest close", f"{summary['latest_close']:,.2f}")
                b.metric("Period return", f"{summary['total_return_pct']:.2f}%")
                c.metric("Annualized volatility", f"{summary['annualized_volatility_pct']:.2f}%")
                d.metric("Observations", summary["observations"])

                st.subheader("Closing price and moving averages")
                chart_df = df.reset_index()
                fig = px.line(chart_df, x="Date", y=["Close", "SMA_20", "SMA_50"], title=ticker)
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("Daily returns")
                ret = chart_df.dropna(subset=["Daily_Return"])
                fig2 = px.histogram(ret, x="Daily_Return", nbins=40)
                st.plotly_chart(fig2, use_container_width=True)

                st.subheader("Analysis summary")
                st.write(summary)
                st.download_button("Download analyzed CSV", df.to_csv().encode("utf-8"),
                                   file_name=f"{ticker.lower()}_analysis.csv", mime="text/csv")
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
