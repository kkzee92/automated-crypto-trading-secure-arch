"""Main entry point for the trading information system."""
import argparse
from src.config import Config
from src.data.market_data import MarketData
from src.strategies.asset_class_strategies import (
    StoreOfValueStrategy, PlatformTokenStrategy,
    StablecoinStrategy, HighVolatilityAltStrategy
)
from src.security.audit import log_action

def run_system(paper: bool = True):
    Config.PAPER_TRADING = paper
    Config.validate()
    log_action("system_start", {"paper_trading": paper, "exchange": Config.EXCHANGE_ID})

    data = MarketData()
    strategies = [
        StoreOfValueStrategy("BTC/USDT"),
        PlatformTokenStrategy("ETH/USDT"),
        HighVolatilityAltStrategy("SOL/USDT"),
        # Stablecoin example (may need different pair depending on exchange)
    ]

    for strat in strategies:
        try:
            ohlcv = data.fetch_ohlcv(strat.symbol, "1h", 100)
            signal = strat.generate_signal(ohlcv)
            risk = strat.risk_params()
            log_action("strategy_signal", {
                "symbol": strat.symbol,
                "asset_class": strat.asset_class,
                "signal": signal,
                "risk_params": risk
            })
            print(f"{strat.symbol} ({strat.asset_class}): {signal}")
            # In full system: place paper or live order here with risk checks
        except Exception as e:
            log_action("strategy_error", {"symbol": strat.symbol, "error": str(e)})

    log_action("system_cycle_complete", {})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Crypto Trading Information System")
    parser.add_argument("--paper", action="store_true", default=True, help="Run in paper trading mode")
    parser.add_argument("--live", action="store_true", help="Enable live trading (requires keys and confirmation)")
    args = parser.parse_args()
    paper_mode = not args.live
    if args.live:
        confirm = input("WARNING: Live trading enabled. Type 'YES' to confirm: ")
        if confirm != "YES":
            print("Aborted.")
            exit(1)
    run_system(paper=paper_mode)
