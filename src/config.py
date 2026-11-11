"""Secure configuration loading."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    EXCHANGE_ID = os.getenv("EXCHANGE_ID", "binance")
    API_KEY = os.getenv("API_KEY", "")
    API_SECRET = os.getenv("API_SECRET", "")
    API_PASSWORD = os.getenv("API_PASSWORD", "")
    PAPER_TRADING = os.getenv("PAPER_TRADING", "true").lower() == "true"
    MAX_POSITION_PCT = float(os.getenv("MAX_POSITION_PCT", "0.02"))
    DEFAULT_STOP_LOSS_PCT = float(os.getenv("DEFAULT_STOP_LOSS_PCT", "0.05"))

    @classmethod
    def validate(cls):
        if not cls.PAPER_TRADING and (not cls.API_KEY or not cls.API_SECRET):
            raise ValueError("Live trading requires API_KEY and API_SECRET in environment.")
        if cls.API_KEY and len(cls.API_KEY) < 10:
            raise ValueError("API_KEY appears invalid.")
        return True
