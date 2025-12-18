# 💰 Pricing

## Pay-Per-Request Model

NODO x402 uses a pay-per-request model. No subscriptions, no minimums, no unused credits.

---

## Pricing Table

### AI Analysis

| Tier | Price | AI Models | Response Time | Best For |
|------|-------|-----------|---------------|----------|
| **Quick** | $0.01 | 1 (Claude) | ~2s | Quick checks |
| **Standard** | $0.05 | 3 models | ~5s | Regular use |
| **Deep** | $0.10 | 6 models | ~10s | Important decisions |

### Scanners

| Service | Price | Description |
|---------|-------|-------------|
| **Yield Scanner** | $0.005 | Find 95%+ probability opportunities |
| **Delta Scanner** | $0.01 | Find logical mispricing |
| **Smart Analyzer** | $0.02 | Category-specific analysis |
| **Arbitrage Scanner** | $0.01 | Find YES+NO < $1.00 |

### Data

| Service | Price | Description |
|---------|-------|-------------|
| **Market Data** | $0.001 | Raw market data |
| **Webhook Alert** | $0.005 | Per alert delivered |

---

## Tier Details

### Quick ($0.01)

- **1 AI Model**: Claude Opus
- **Response Time**: ~2 seconds
- **Use Case**: Fast validation, quick checks
- **Output**: Single model analysis

### Standard ($0.05)

- **3 AI Models**: Claude + GPT-4o + Gemini
- **Response Time**: ~5 seconds
- **Use Case**: Regular trading decisions
- **Output**: Consensus from 3 models

### Deep ($0.10)

- **6 AI Models**: Full consensus
  - Claude Opus (Anthropic)
  - GPT-4o (OpenAI)
  - Gemini Pro (Google)
  - Llama 405B (Meta)
  - DeepSeek V3
  - Mistral Large
- **Response Time**: ~10 seconds
- **Use Case**: High-stakes decisions
- **Output**: Full consensus + dissent analysis

---

## Volume Discounts

| Monthly Spend | Discount |
|---------------|----------|
| $0 - $10 | 0% |
| $10 - $50 | 10% |
| $50 - $100 | 15% |
| $100+ | 20% |

Discounts are applied automatically based on your wallet's monthly usage.

---

## Cost Examples

### Casual User

```
Weekly usage:
- 5x Deep analysis     = $0.50
- 10x Yield scans      = $0.05
- 20x Market data      = $0.02
─────────────────────────────
Weekly total            $0.57
Monthly total          ~$2.28
```

### Active Trader

```
Daily usage:
- 3x Deep analysis     = $0.30
- 5x Standard analysis = $0.25
- 10x Yield scans      = $0.05
- 5x Delta scans       = $0.05
- 50x Market data      = $0.05
─────────────────────────────
Daily total             $0.70
Monthly total         ~$21.00
(with 10% discount)   ~$18.90
```

### Trading Bot

```
Hourly usage:
- 2x Quick analysis    = $0.02
- 1x Yield scan        = $0.005
- 10x Market data      = $0.01
─────────────────────────────
Hourly total            $0.035
Daily total             $0.84
Monthly total         ~$25.20
(with 10% discount)   ~$22.68
```

---

## Comparison to Alternatives

| Service | NODO x402 | Traditional API |
|---------|-----------|-----------------|
| Minimum | $0.001 | $10-100/month |
| Unused credits | N/A | Lost |
| Setup time | Seconds | Days |
| Payment | Per request | Monthly |
| Geographic | Global | Limited |

---

## Payment Details

- **Currency**: USDC (Solana SPL)
- **Network**: Solana Mainnet
- **Finality**: ~400ms
- **Transaction Fee**: ~$0.00025

### USDC Addresses

- **Mainnet USDC Mint**: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- **Devnet USDC Mint**: `4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU`

---

## Free Endpoints

These endpoints don't require payment:

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info |
| `GET /health` | Health check |
| `GET /x402/info` | Payment info |
| `GET /account/balance` | Check balance |
| `GET /account/usage` | Usage stats |
| `GET /account/pricing` | Pricing info |
| `GET /analyze/tiers` | Tier info |

---

## Getting USDC

### From Exchanges

1. Buy USDC on Coinbase, Binance, Kraken
2. Withdraw to Solana address

### Bridge from Other Chains

- [Portal Bridge](https://portalbridge.com/)
- [Wormhole](https://wormhole.com/)

### Swap SOL to USDC

- [Jupiter](https://jup.ag/)
- [Raydium](https://raydium.io/)

