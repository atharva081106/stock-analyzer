import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import pandas as pd

def plot_prices(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price'))
    fig.update_layout(title='Historical Closing Prices', xaxis_title='Date', yaxis_title='Price')
    return fig

def plot_prediction(pred_df):
    fig = px.line(pred_df, x='Date', y=pred_df.columns[1], title="Predicted Closing Price")
    return fig

def plot_multi_stock(tickers):
    fig = go.Figure()
    for ticker in tickers:
        try:
            df = yf.download(ticker.strip(), period="6mo", interval="1d")
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=ticker.upper()))
        except:
            continue

    fig.update_layout(
        title="📈 Historical Closing Prices",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark"
    )
    return fig

def plot_performance_comparison(tickers):
    import yfinance as yf
    import pandas as pd

    df_all = pd.DataFrame()

    for ticker in tickers:
        try:
            data = yf.download(ticker.strip(), period="6mo", interval="1d")['Close']
            data = data / data.iloc[0] * 100  # Normalize to 100
            df_all[ticker.upper()] = data
        except:
            continue

    fig = px.line(df_all, x=df_all.index, y=df_all.columns,
                  labels={'value': 'Normalized Price (Base = 100)', 'index': 'Date'},
                  title='📊 Performance Comparison (% Gain from Starting Point)')
    fig.update_layout(template="plotly_dark")
    return fig

def plot_single_stock_performance(df, ticker="Stock"):
    import pandas as pd
    import plotly.express as px

    # Handle multi-index columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns]

    df = df.copy()

    # Ensure Date is present
    if 'Date' not in df.columns:
        df = df.reset_index()

    # Try to find a 'Close' column
    close_col = None
    for col in df.columns:
        if 'close' in col.lower():
            close_col = col
            break

    if close_col is None:
        raise KeyError("Could not find a 'Close' column in DataFrame.")

    df['Normalized'] = df[close_col] / df[close_col].iloc[0] * 100

    fig = px.line(df, x='Date', y='Normalized',
                  title=f"📈 {ticker.upper()} Performance (Normalized to 100)")
    fig.update_layout(xaxis_title="Date", yaxis_title="Normalized Price", template="plotly_dark")
    return fig

