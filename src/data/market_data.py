"""Market data fetching with rate limiting and error handling."""
import time
import ccxt
from src.config import Config
from src.security.audit import log_action

class MarketData:
    def __init__(self):
        exchange_class = getattr(ccxt, Config.EXCHANGE_ID)
        self.exchange = exchange_class({
            "apiKey": Config.API_KEY,
            "secret": Config.API_SECRET,
            "password": Config.API_PASSWORD or None,
            "enableRateLimit": True,
            "options": {"adjustForTimeDifference": True}
        })
        if Config.PAPER_TRADING:
            # Sandbox / testnet where available
            if hasattr(self.exchange, "set_sandbox_mode"):
                try:
                    self.exchange.set_sandbox_mode(True)
                except Exception:
                    pass

    def fetch_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 100):
        """Fetch OHLCV with retry."""
        for attempt in range(3):
            try:
                data = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                log_action("fetch_ohlcv", {"symbol": symbol, "timeframe": timeframe, "candles": len(data)})
                return data
            except Exception as e:
                log_action("fetch_error", {"symbol": symbol, "error": str(e), "attempt": attempt})
                time.sleep(2 ** attempt)
        raise RuntimeError(f"Failed to fetch {symbol} after retries")

    def fetch_ticker(self, symbol: str):
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            log_action("fetch_ticker", {"symbol": symbol, "last": ticker.get("last")})
            return ticker
        except Exception as e:
            log_action("ticker_error", {"symbol": symbol, "error": str(e)})
            raise
