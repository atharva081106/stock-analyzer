def summarize(df):
    return {
        "Min Price": round(df['Close'].min(), 2),
        "Max Price": round(df['Close'].max(), 2),
        "Mean Price": round(df['Close'].mean(), 2),
        "Median": round(df['Close'].median(), 2),
        "Std Dev": round(df['Close'].std(), 2)
    }
