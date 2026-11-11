# Automated Cryptocurrency Trading Information System

**Educational & Research Framework** — Not financial advice. Use at your own risk. Always test with paper trading.

This repository provides a modular, security-first framework for automated cryptocurrency trading information systems. It includes:

- Multi-exchange data aggregation via CCXT
- Asset-class-specific trading strategies (Store-of-Value, Platform tokens, Stablecoins, High-volatility Alts)
- Robust cyber and data security architecture
- Audit logging, rate limiting, and secure credential handling
- Paper trading mode by default

## Key Principles

1. **Security First**: API keys never committed, withdrawal permissions disabled, IP whitelisting recommended, audit trails.
2. **Asset-Class Awareness**: Strategies adapted to characteristics of BTC (SoV), ETH (smart contracts), stables (low vol), alts (high vol).
3. **Risk Management**: Position sizing, stop-losses, max drawdown controls.
4. **Transparency**: All actions logged; open-source for review.

## Quick Start

```bash
git clone https://github.com/kkzee92/automated-crypto-trading-secure-arch.git
cd automated-crypto-trading-secure-arch
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys (trade-only, no withdrawal)
python -m src.main --paper
```

## Security Checklist

- [ ] API keys have trade + read only (NO withdrawal)
- [ ] IP allowlist configured on exchange
- [ ] Dedicated sub-account with limited capital
- [ ] .env in .gitignore and never committed
- [ ] 2FA enabled on exchange accounts
- [ ] Regular key rotation
- [ ] Review audit logs periodically

See `SECURITY.md` and `docs/architecture.md` for details.

## Disclaimer

This software is provided for educational and research purposes only. Cryptocurrency trading involves substantial risk of loss. Past performance is not indicative of future results. The authors and contributors assume no liability for any trading losses or damages.

## License

MIT License
