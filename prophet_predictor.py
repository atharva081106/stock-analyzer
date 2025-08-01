import pandas as pd
from prophet import Prophet
from datetime import datetime

def forecast_with_prophet(df, days=5):
    # Prepare data for Prophet
    df = df[['Date', 'Close']].copy()
    df.columns = ['ds', 'y']
    df['ds'] = pd.to_datetime(df['ds'])

    # Create and fit the model
    model = Prophet(daily_seasonality=True)
    model.fit(df)

    # Forecast future
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    # Extract the last N days of forecast
    result = forecast[['ds', 'yhat']].tail(days)
    result.columns = ['Date', 'Predicted Close']

    # Ensure 'Predicted Close' is a flat 1D float column
    result['Predicted Close'] = result['Predicted Close'].astype(float)

    return result
