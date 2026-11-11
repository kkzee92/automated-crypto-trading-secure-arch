# System Architecture

## High-Level Design

```
+------------------+     +-------------------+     +------------------+
|  Market Data     | --> |  Strategy Engine  | --> |  Risk Manager    |
|  (CCXT + Cache)  |     |  (Asset-Class)    |     |  + Order Executor|
+------------------+     +-------------------+     +------------------+
         |                        |                          |
         v                        v                          v
+------------------+     +-------------------+     +------------------+
|  Audit Logger    |     |  Config / Secrets |     |  Paper / Live    |
|  (Structured)    |     |  (Env / .env)     |     |  Mode Switch     |
+------------------+     +-------------------+     +------------------+
```

## Components

1. **Market Data Layer**: Fetches OHLCV, tickers. Rate-limited, retries, sandbox support.
2. **Strategy Layer**: Pluggable strategies classified by asset type:
   - Store of Value (BTC): Momentum / DCA hybrid
   - Platform (ETH, SOL): Trend + RSI
   - Stablecoin: Depeg monitoring / info
   - High-Vol Alt: Mean reversion with tighter sizing
3. **Security Layer**: Credential isolation, audit, validation.
4. **Execution Layer**: Paper by default; live requires explicit confirmation.

## Data Flow

1. Load secure config
2. Initialize exchange client (rate limit on)
3. For each monitored asset/strategy:
   - Fetch recent candles
   - Generate signal
   - Apply risk parameters
   - Log + (optionally) execute
4. Cycle complete; sleep / schedule next

## Extensibility

- Add new asset class by subclassing `BaseStrategy` and registering.
- Swap exchanges via CCXT.
- Integrate additional data sources (on-chain, sentiment) in data layer.
- Future: ML signal enhancement, portfolio optimizer.

## Security Integration

Every data fetch and signal is audited. Secrets never leave the process boundary except to the exchange API over TLS.
