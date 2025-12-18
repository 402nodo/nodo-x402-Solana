# 📡 API Reference

## Base URL

```
https://api.nodo.ai/x402/v1
```

---

## Authentication

All paid endpoints use x402 payment authentication:

1. Make request without payment
2. Receive 402 with payment details
3. Send USDC payment on Solana
4. Retry with `X-Payment-Tx` header

```bash
curl -X POST https://api.nodo.ai/x402/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-Payment-Tx: YOUR_SOLANA_TX_SIGNATURE" \
  -d '{"market": "..."}'
```

---

## Endpoints

### POST /analyze

Multi-AI consensus analysis for prediction markets.

**Price:** $0.01 - $0.10 (based on tier)

**Request:**
```json
{
  "market": "polymarket.com/event/btc-150k-2025",
  "strategy": "yield_farming",
  "tier": "deep"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `market` | string | Yes | Market URL or ID |
| `strategy` | string | No | `yield_farming`, `delta_neutral`, `momentum` |
| `tier` | string | No | `quick` ($0.01), `standard` ($0.05), `deep` ($0.10) |

**Response (200):**
```json
{
  "market": {
    "question": "Will Bitcoin reach $150,000 by Dec 31, 2025?",
    "yes_price": 0.08,
    "no_price": 0.92,
    "volume": 1250000,
    "end_date": "2025-12-31",
    "url": "https://polymarket.com/event/..."
  },
  "analysis": {
    "consensus": "BUY_NO",
    "agreement": "5/6",
    "confidence": 82,
    "action": "Buy NO position",
    "potential_profit": "8.7%",
    "apy": "45%"
  },
  "models": [
    {
      "name": "claude-opus",
      "action": "BUY_NO",
      "confidence": 85,
      "reasoning": "BTC would need 50% growth in 14 days..."
    },
    {
      "name": "gpt-4o",
      "action": "BUY_NO",
      "confidence": 80,
      "reasoning": "Historical data suggests..."
    }
  ],
  "dissent": {
    "model": "gemini-pro",
    "action": "SKIP",
    "reason": "Macro uncertainty..."
  },
  "risks": [
    "Black swan events could cause rapid price movement",
    "Market sentiment can shift quickly"
  ],
  "meta": {
    "request_id": "req_abc123",
    "cost": "$0.10",
    "processing_time": "8.2s",
    "models_used": 6,
    "tier": "deep"
  }
}
```

---

### GET /yield/scan

Scan for yield farming opportunities (high probability events).

**Price:** $0.005

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `min_probability` | float | 0.95 | Minimum probability (0.5-0.99) |
| `min_volume` | float | 5000 | Minimum market volume ($) |
| `max_days` | int | 30 | Maximum days to resolution |
| `risk_level` | string | - | Filter: `LOW`, `MEDIUM`, `HIGH` |
| `limit` | int | 20 | Maximum results (1-100) |

**Response:**
```json
{
  "opportunities": [
    {
      "market_id": "abc123",
      "question": "Will the sun rise tomorrow?",
      "outcome": "YES",
      "buy_price": 0.97,
      "profit_pct": 3.09,
      "apy": 112.8,
      "days_to_resolution": 10,
      "volume": 150000,
      "risk_level": "LOW",
      "url": "https://polymarket.com/event/..."
    }
  ],
  "total": 15,
  "filters": {
    "min_probability": 0.95,
    "min_volume": 5000
  },
  "meta": {
    "price": "$0.005",
    "source": "polymarket"
  }
}
```

---

### GET /delta/scan

Scan for delta neutral / mispricing opportunities.

**Price:** $0.01

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `min_profit` | float | 5.0 | Minimum profit potential (%) |
| `min_confidence` | int | 50 | Minimum confidence (0-100) |
| `topic` | string | - | Filter: `BTC`, `ETH`, `TRUMP`, etc |
| `limit` | int | 20 | Maximum results |

**Response:**
```json
{
  "opportunities": [
    {
      "topic": "BTC",
      "logic_error": "$150K YES ($0.20) > $100K YES ($0.15)",
      "profit_potential": 33.3,
      "confidence": 90,
      "action": "BUY '$100K' YES",
      "explanation": "If BTC reaches $150K, it must pass $100K first...",
      "event_a": {
        "question": "Will BTC reach $150K?",
        "yes_price": 0.20,
        "no_price": 0.80,
        "url": "..."
      },
      "event_b": {
        "question": "Will BTC reach $100K?",
        "yes_price": 0.15,
        "no_price": 0.85,
        "url": "..."
      }
    }
  ],
  "total": 5,
  "meta": {
    "price": "$0.01"
  }
}
```

---

### POST /smart/analyze

Smart category-specific analysis.

**Price:** $0.02

**Request:**
```json
{
  "question": "Will Bitcoin reach $200,000 by December 31, 2025?",
  "current_price": 0.15,
  "outcome": "NO",
  "days_left": 14
}
```

**Response:**
```json
{
  "category": "crypto_price",
  "confidence_score": 70,
  "predicted_outcome": "NO",
  "verdict": "NO very likely - 100% growth unrealistic in 14 days",
  "reasons": [
    "Needs 100% growth (more than 2x)",
    "Current BTC: $100,000",
    "In 14 days this is practically impossible"
  ],
  "risks": [
    "Crypto markets are highly volatile",
    "News can rapidly change prices"
  ],
  "data_used": {
    "target_price": 200000,
    "current_price": 100000,
    "change_needed": "+100%"
  }
}
```

---

### GET /arbitrage/scan

Scan for intra-platform arbitrage (YES + NO < $1).

**Price:** $0.01

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `min_profit` | float | 0.5 | Minimum profit (%) |
| `min_volume` | float | 1000 | Minimum volume ($) |
| `limit` | int | 20 | Maximum results |

**Response:**
```json
{
  "opportunities": [
    {
      "market_question": "Will event X happen?",
      "yes_price": 0.45,
      "no_price": 0.50,
      "total_cost": 0.95,
      "guaranteed_profit": 0.05,
      "profit_pct": 5.26,
      "volume": 50000,
      "url": "..."
    }
  ],
  "total": 3
}
```

---

### GET /markets

Get market data from prediction platforms.

**Price:** $0.001

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `platform` | string | polymarket | `polymarket`, `kalshi` |
| `active` | bool | true | Only active markets |
| `min_volume` | float | 0 | Minimum volume ($) |
| `search` | string | - | Search in question |
| `limit` | int | 50 | Maximum results |

**Response:**
```json
{
  "markets": [
    {
      "id": "abc123",
      "question": "Will BTC reach $150K?",
      "yes_price": 0.08,
      "no_price": 0.92,
      "volume": 1250000,
      "platform": "polymarket",
      "url": "..."
    }
  ],
  "total": 156
}
```

---

### POST /webhooks

Create webhook subscription for alerts.

**Price:** $0.005 per alert sent

**Request:**
```json
{
  "url": "https://yoursite.com/webhook",
  "events": ["opportunity.yield", "opportunity.delta"],
  "filters": {
    "min_profit": 5.0,
    "topics": ["BTC", "ETH"]
  }
}
```

**Events:**
- `opportunity.yield` - New yield opportunity
- `opportunity.delta` - New mispricing
- `opportunity.arbitrage` - New arbitrage
- `market.resolved` - Market resolved

---

## Free Endpoints

These endpoints don't require payment:

### GET /health
```json
{"status": "healthy", "solana_connected": true}
```

### GET /x402/info
```json
{
  "x402_version": 1,
  "network": "solana-mainnet",
  "currency": "USDC",
  "recipient": "NoDo...",
  "supported_endpoints": [...]
}
```

### GET /account/balance
### GET /account/usage
### GET /account/pricing

---

## Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `PAYMENT_REQUIRED` | 402 | Payment needed |
| `PAYMENT_INVALID` | 402 | Payment verification failed |
| `INVALID_MARKET` | 400 | Market not found |
| `INVALID_PARAMS` | 400 | Bad request parameters |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Rate Limits

| Tier | Requests/min | Requests/day |
|------|--------------|--------------|
| Free endpoints | 60 | 10,000 |
| Paid endpoints | 120 | Unlimited |

Rate limits are per wallet address.

