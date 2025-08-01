import yfinance as yf
import pandas as pd

def compare_stocks(tickers):
    rows = []
    for ticker in tickers:
        ticker = ticker.strip().upper()
        try:
            df = yf.download(ticker, period="6mo", interval="1d")
            close = df['Close']
            rows.append({
                "Ticker": ticker,
                "Current Price": round(float(close.iloc[-1]), 2),
                "Max": round(float(close.max()), 2),
                "Min": round(float(close.min()), 2),
                "Mean": round(float(close.mean()), 2)
            })
        except Exception as e:
            rows.append({
                "Ticker": ticker,
                "Current Price": "Error",
                "Max": "Error",
                "Min": "Error",
                "Mean": str(e)
            })

    return pd.DataFrame(rows).set_index("Ticker")
