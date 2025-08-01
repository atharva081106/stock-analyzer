import pandas as pd
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor, XGBClassifier
from sklearn.model_selection import train_test_split
from datetime import datetime

def get_future_trading_days(start_date, n):
    future = []
    current = start_date
    while len(future) < n:
        current += pd.Timedelta(days=1)
        if current.weekday() < 5:
            future.append(current)
    return future

def engineer_features(df, window=5):
    df['Return_1D'] = df['Close'].pct_change()
    df['MA_5'] = df['Close'].rolling(5).mean()
    df['MA_10'] = df['Close'].rolling(10).mean()
    df['Volatility'] = df['Close'].rolling(5).std()
    for i in range(1, window + 1):
        df[f'lag_{i}'] = df['Close'].shift(i)
    return df.dropna()

def train_linear_model(df, days_ahead=5):
    # Flatten multi-index columns if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns]

    # Reset index to get Date column
    if 'Date' not in df.columns:
        df = df.reset_index()

    # Detect the correct Close column
    close_col = next((col for col in df.columns if 'Close' in col), None)
    if not close_col:
        raise ValueError("No 'Close' column found.")

    df = df[['Date', close_col]].copy()
    df.columns = ['Date', 'Close']  # rename for simplicity

    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df['Date_Ordinal'] = df['Date'].map(pd.Timestamp.toordinal)

    model = LinearRegression()
    model.fit(df[['Date_Ordinal']], df['Close'])

    today = pd.Timestamp(datetime.today().date())
    future_dates = []
    while len(future_dates) < days_ahead:
        today += pd.Timedelta(days=1)
        if today.weekday() < 5:
            future_dates.append(today)

    ordinals = [[d.toordinal()] for d in future_dates]
    preds = model.predict(ordinals)

    return pd.DataFrame({'Date': future_dates, 'Predicted Close': preds})

def train_xgboost_model(df, days=5):
    df = engineer_features(df)
    df['Target'] = df['Close'].shift(-1)
    df.dropna(inplace=True)

    X = df.drop(columns=['Date', 'Close', 'Target'])
    y = df['Target']
    X_train, _, y_train, _ = train_test_split(X, y, shuffle=False, test_size=0.2)

    model = XGBRegressor(n_estimators=100, learning_rate=0.1)
    model.fit(X_train, y_train)

    recent = df.tail(days).drop(columns=['Date', 'Close', 'Target'])
    preds = model.predict(recent)

    future_dates = get_future_trading_days(pd.Timestamp(datetime.today().date()), days)
    return pd.DataFrame({'Date': future_dates, 'Predicted Close': preds.flatten() if hasattr(preds, 'flatten') else list(preds)})

def predict_direction(df, days=5):
    df = engineer_features(df)
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    df.dropna(inplace=True)

    X = df.drop(columns=['Date', 'Close', 'Target'])
    y = df['Target']
    X_train, _, y_train, _ = train_test_split(X, y, shuffle=False, test_size=0.2)

    model = XGBClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    future_dates = get_future_trading_days(pd.Timestamp(datetime.today().date()), days)
    preds = model.predict(df.tail(days).drop(columns=['Date', 'Close', 'Target']))
    labels = ['Up' if p == 1 else 'Down' for p in preds]

    return pd.DataFrame({'Date': future_dates, 'Direction': labels})

def engineer_features(df):
    # 🔄 Handle MultiIndex columns like ('Close', 'AAPL')
    if isinstance(df.columns, pd.MultiIndex):
        if 'Close' in df.columns.get_level_values(0):
            df.columns = df.columns.droplevel(1)  # Drop the ticker level if present
        else:
            df.columns = [col[0] for col in df.columns]  # Simplify MultiIndex

    # ✅ Ensure 'Close' column exists
    if 'Close' not in df.columns:
        raise ValueError("Expected 'Close' column not found in DataFrame!")

    df['Return_1D'] = df['Close'].pct_change()
    df['Return_5D'] = df['Close'].pct_change(5)
    df['SMA_5'] = df['Close'].rolling(5).mean()
    df['SMA_10'] = df['Close'].rolling(10).mean()
    df['Volatility'] = df['Close'].rolling(5).std()
    df = df.dropna()

    return df
