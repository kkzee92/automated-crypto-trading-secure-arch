"""Asset-class-specific trading strategies."""
import numpy as np
from .base import BaseStrategy

class StoreOfValueStrategy(BaseStrategy):
    """BTC-like: Longer-term DCA + momentum filter. Lower frequency, tighter risk."""
    def __init__(self, symbol: str = "BTC/USDT"):
        super().__init__(symbol, "store_of_value")

    def generate_signal(self, ohlcv: list) -> dict:
        if len(ohlcv) < 50:
            return {"action": "hold", "confidence": 0.0, "reason": "insufficient data"}
        closes = np.array([c[4] for c in ohlcv])
        sma_20 = np.mean(closes[-20:])
        sma_50 = np.mean(closes[-50:])
        current = closes[-1]
        # Momentum: price above both SMAs
        if current > sma_20 > sma_50:
            return {"action": "buy", "confidence": 0.7, "reason": "bullish momentum on SoV asset"}
        elif current < sma_20 < sma_50:
            return {"action": "sell", "confidence": 0.6, "reason": "bearish momentum"}
        return {"action": "hold", "confidence": 0.5, "reason": "neutral"}

    def risk_params(self) -> dict:
        return {"max_position_pct": 0.05, "stop_loss_pct": 0.08}  # Slightly higher allocation for core asset

class PlatformTokenStrategy(BaseStrategy):
    """ETH / L1: Trend following with RSI filter."""
    def __init__(self, symbol: str = "ETH/USDT"):
        super().__init__(symbol, "platform")

    def generate_signal(self, ohlcv: list) -> dict:
        if len(ohlcv) < 30:
            return {"action": "hold", "confidence": 0.0, "reason": "insufficient data"}
        closes = np.array([c[4] for c in ohlcv])
        # Simple RSI-like
        deltas = np.diff(closes)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains[-14:]) if len(gains) >= 14 else 0
        avg_loss = np.mean(losses[-14:]) if len(losses) >= 14 else 0
        rs = avg_gain / avg_loss if avg_loss != 0 else 100
        rsi = 100 - (100 / (1 + rs))
        current = closes[-1]
        sma_20 = np.mean(closes[-20:])
        if rsi < 30 and current > sma_20:
            return {"action": "buy", "confidence": 0.65, "reason": "oversold bounce on platform token"}
        elif rsi > 70:
            return {"action": "sell", "confidence": 0.6, "reason": "overbought"}
        return {"action": "hold", "confidence": 0.5, "reason": "neutral RSI"}

    def risk_params(self) -> dict:
        return {"max_position_pct": 0.03, "stop_loss_pct": 0.06}

class StablecoinStrategy(BaseStrategy):
    """Stablecoins: Monitor depeg or yield opportunities (info system focus)."""
    def __init__(self, symbol: str = "USDT/USD"):
        super().__init__(symbol, "stablecoin")

    def generate_signal(self, ohlcv: list) -> dict:
        # For stables, focus on price stability info
        if not ohlcv:
            return {"action": "hold", "confidence": 1.0, "reason": "stable"}
        closes = [c[4] for c in ohlcv[-10:]]
        avg = np.mean(closes)
        if abs(avg - 1.0) > 0.01:  # depeg warning
            return {"action": "alert", "confidence": 0.9, "reason": f"potential depeg, avg={avg:.4f}"}
        return {"action": "hold", "confidence": 0.95, "reason": "stable price"}

    def risk_params(self) -> dict:
        return {"max_position_pct": 0.1, "stop_loss_pct": 0.02}

class HighVolatilityAltStrategy(BaseStrategy):
    """Alts: Mean reversion or breakout with tight risk."""
    def __init__(self, symbol: str = "SOL/USDT"):
        super().__init__(symbol, "high_vol_alt")

    def generate_signal(self, ohlcv: list) -> dict:
        if len(ohlcv) < 20:
            return {"action": "hold", "confidence": 0.0, "reason": "insufficient data"}
        closes = np.array([c[4] for c in ohlcv])
        sma = np.mean(closes[-20:])
        std = np.std(closes[-20:])
        current = closes[-1]
        zscore = (current - sma) / std if std > 0 else 0
        if zscore < -1.5:
            return {"action": "buy", "confidence": 0.55, "reason": "mean reversion opportunity on alt"}
        elif zscore > 1.5:
            return {"action": "sell", "confidence": 0.55, "reason": "overextended"}
        return {"action": "hold", "confidence": 0.4, "reason": "within band"}

    def risk_params(self) -> dict:
        return {"max_position_pct": 0.01, "stop_loss_pct": 0.10}  # Smaller size, wider stop for vol
