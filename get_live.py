import yfinance as yf

def get_live_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "symbol": info.get("symbol", ticker),
            "price": info.get("regularMarketPrice", None),
            "currency": info.get("currency", ""),
            "time": info.get("regularMarketTime", "")
        }
    except Exception as e:
        return {"error": str(e)}
