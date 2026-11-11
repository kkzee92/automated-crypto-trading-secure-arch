"""Base strategy interface."""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseStrategy(ABC):
    def __init__(self, symbol: str, asset_class: str):
        self.symbol = symbol
        self.asset_class = asset_class

    @abstractmethod
    def generate_signal(self, ohlcv: list) -> Dict[str, Any]:
        """Return signal dict: action (buy/sell/hold), confidence, reason."""
        pass

    def risk_params(self) -> Dict[str, float]:
        """Asset-class specific risk parameters."""
        return {"max_position_pct": 0.02, "stop_loss_pct": 0.05}
