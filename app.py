import streamlit as st
from data_fetcher import fetch_data
from predictor import train_linear_model, train_xgboost_model, predict_direction
from prophet_predictor import forecast_with_prophet
from analytics import summarize
from charts import (
    plot_prices,
    plot_prediction,
    plot_multi_stock,
    plot_performance_comparison,
    plot_single_stock_performance
)
from compare import compare_stocks
from get_live import get_live_price
from notify import send_telegram_message
import pandas as pd

st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")

st.title("📊 Stock Analyzer & Forecaster")
st.markdown("Analyze, compare, and forecast stock trends with smart ML-powered insights.")

# ─────────────────────────────────────────────────────────────
# Sidebar Controls
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Control Panel")
    option = st.radio("Select View", ["Single Stock", "Compare Stocks", "Live Price"])
    st.markdown("---")

# ─────────────────────────────────────────────────────────────
# Single Stock Mode
# ─────────────────────────────────────────────────────────────
if option == "Single Stock":
    with st.sidebar:
        ticker = st.text_input("🔎 Enter Ticker Symbol", "AAPL").upper()
        days_ahead = st.slider("📅 Days to Predict", 1, 10, 5)
        model_type = st.selectbox("🤖 Prediction Model", ["Linear", "XGBoost", "Prophet", "Direction"])
        send_alert = st.checkbox("🔔 Send to Telegram (if configured)")
        run = st.button("🚀 Run Analysis")

    if run and ticker:
        with st.spinner("📡 Fetching data..."):
            df = fetch_data(ticker)
            st.write("ℹ️ Columns in data:", df.columns)  # Debugging aid

        st.subheader(f"📈 Stock: {ticker}")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 🔢 Latest 5 Days")
            st.dataframe(df.tail(), use_container_width=True)
        with col2:
            st.markdown("### 📊 Summary Stats")
            st.json(summarize(df))

        st.markdown("### 📉 Historical Price Chart")
        st.plotly_chart(plot_prices(df), use_container_width=True)

        st.markdown("### 📈 Performance Since Start (Base = 100)")
        st.plotly_chart(plot_single_stock_performance(df, ticker), use_container_width=True)

        with st.spinner("🔮 Generating predictions..."):
            if model_type == "Linear":
                pred_df = train_linear_model(df, days_ahead)
                st.markdown("### 🔮 Linear Regression Prediction")
                st.plotly_chart(plot_prediction(pred_df), use_container_width=True)
                st.download_button("⬇️ Download Linear Forecast", pred_df.to_csv(index=False), file_name="linear_forecast.csv")
            elif model_type == "XGBoost":
                pred_df = train_xgboost_model(df, days_ahead)
                st.markdown("### 🔮 XGBoost Prediction")
                st.plotly_chart(plot_prediction(pred_df), use_container_width=True)
                st.download_button("⬇️ Download XGBoost Forecast", pred_df.to_csv(index=False), file_name="xgboost_forecast.csv")
            elif model_type == "Prophet":
                pred_df = forecast_with_prophet(df, days_ahead)
                st.markdown("### 🔮 Prophet Prediction")
                st.plotly_chart(plot_prediction(pred_df), use_container_width=True)
                st.download_button("⬇️ Download Prophet Forecast", pred_df.to_csv(index=False), file_name="prophet_forecast.csv")
            else:
                pred_df = predict_direction(df, days_ahead)
                st.markdown("### 🧭 Direction Forecast (Up/Down)")
                st.dataframe(pred_df, use_container_width=True)
                st.download_button("⬇️ Download Direction Prediction", pred_df.to_csv(index=False), file_name="direction_forecast.csv")

            if send_alert:
                send_telegram_message(f"📈 Stock Alert: {ticker} - {model_type} model run for {days_ahead} days!")

# ─────────────────────────────────────────────────────────────
# Compare Mode
# ─────────────────────────────────────────────────────────────
elif option == "Compare Stocks":
    st.subheader("📊 Multi-Stock Comparison")
    tickers = st.text_input("Enter tickers separated by commas", "AAPL,MSFT,GOOGL").split(",")

    if st.button("🔍 Compare"):
        with st.spinner("Loading stock data..."):
            result = compare_stocks(tickers)
            numeric_cols = result.select_dtypes(include='number').columns
            st.dataframe(result.style.format({col: "{:.2f}" for col in numeric_cols}), use_container_width=True)

            st.markdown("### 📈 Historical Price Comparison")
            st.plotly_chart(plot_multi_stock(tickers), use_container_width=True)

            st.markdown("### 🔼 Performance Comparison (Relative Growth)")
            st.plotly_chart(plot_performance_comparison(tickers), use_container_width=True)

# ─────────────────────────────────────────────────────────────
# Live Mode
# ─────────────────────────────────────────────────────────────
elif option == "Live Price":
    st.subheader("📡 Live Price Checker")
    ticker = st.text_input("Enter symbol for live price", "AAPL").upper()
    if st.button("Get Live Price"):
        info = get_live_price(ticker)
        if "price" in info:
            st.metric(label=f"{ticker} Price", value=f"{info['price']} {info['currency']}")
        else:
            st.error("Couldn't fetch live data.")
