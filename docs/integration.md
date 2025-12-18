# 🔌 Integration Guide

## Quick Start

Get started with NODO x402 in 5 minutes.

---

## Prerequisites

1. **Solana Wallet** with USDC
   - [Phantom](https://phantom.app/)
   - [Solflare](https://solflare.com/)
   - [Backpack](https://backpack.app/)

2. **USDC on Solana**
   - Bridge from other chains
   - Buy on exchanges (Coinbase, Binance)
   - Swap SOL → USDC on Jupiter

---

## Installation

### Python

```bash
pip install nodo-x402

# With Solana support for auto-payments
pip install nodo-x402[solana]
```

### TypeScript / JavaScript

```bash
npm install @nodo-ai/x402

# or
yarn add @nodo-ai/x402

# or
pnpm add @nodo-ai/x402
```

---

## Basic Usage

### Python

```python
import asyncio
from nodo_x402 import NodoClient

async def main():
    # Initialize with your Solana keypair
    client = NodoClient(
        keypair_path="~/.config/solana/id.json"
    )
    
    # Make a request - payment handled automatically
    result = await client.analyze(
        market="polymarket.com/event/btc-150k-2025",
        tier="standard"  # $0.05
    )
    
    print(f"Consensus: {result.consensus}")
    print(f"Confidence: {result.confidence}%")
    
    await client.close()

asyncio.run(main())
```

### TypeScript

```typescript
import { NodoClient } from '@nodo-ai/x402';
import { Keypair } from '@solana/web3.js';
import fs from 'fs';

async function main() {
  // Load keypair
  const secretKey = JSON.parse(
    fs.readFileSync('~/.config/solana/id.json', 'utf8')
  );
  const keypair = Keypair.fromSecretKey(Uint8Array.from(secretKey));

  // Initialize client
  const client = new NodoClient({
    keypair: keypair.secretKey,
  });

  // Make request - payment handled automatically
  const result = await client.analyze({
    market: 'polymarket.com/event/btc-150k-2025',
    tier: 'standard',
  });

  console.log(`Consensus: ${result.analysis.consensus}`);
  console.log(`Confidence: ${result.analysis.confidence}%`);
}

main();
```

---

## Using Individual Services

### Yield Scanner

```python
# Find high-probability opportunities
opportunities = await client.yield_scan(
    min_probability=0.95,  # 95%+ probability
    min_volume=10000,      # $10k+ volume
    max_days=30,           # Resolves within 30 days
    risk_level="LOW",      # Only safe bets
    limit=10
)

for opp in opportunities:
    print(f"{opp.question}")
    print(f"  Buy {opp.outcome} @ ${opp.buy_price:.3f}")
    print(f"  Profit: {opp.profit_pct:.2f}% | APY: {opp.apy:.0f}%")
```

### Delta Scanner

```python
# Find logical mispricing
deltas = await client.delta_scan(
    min_profit=5.0,      # 5%+ profit potential
    min_confidence=70,   # 70%+ confidence
    topic="BTC",         # Filter to Bitcoin
    limit=5
)

for d in deltas:
    print(f"[{d.topic}] {d.logic_error}")
    print(f"  Profit: {d.profit_potential:.1f}%")
    print(f"  Action: {d.action}")
```

### Smart Analyzer

```python
# Category-specific analysis
result = await client.smart_analyze(
    question="Will Trump win the 2028 election?",
    current_price=0.35,
    outcome="YES",
    days_left=1000
)

print(f"Category: {result['category']}")
print(f"Verdict: {result['verdict']}")
for reason in result['reasons']:
    print(f"  - {reason}")
```

### Market Data

```python
# Get markets
markets = await client.get_markets(
    platform="polymarket",
    min_volume=100000,
    search="bitcoin",
    limit=20
)

for m in markets:
    print(f"{m.question}")
    print(f"  YES: ${m.yes_price:.2f} | NO: ${m.no_price:.2f}")
```

---

## Manual Payment Mode

If you want to handle payments yourself:

```python
from nodo_x402 import NodoClient, PaymentRequired

# Disable auto-payment
client = NodoClient(
    keypair_path="~/.config/solana/id.json",
    auto_pay=False
)

try:
    result = await client.analyze(market="...")
except PaymentRequired as e:
    # Payment details
    print(f"Amount: ${e.amount} USDC")
    print(f"Recipient: {e.recipient}")
    print(f"Memo: {e.memo}")
    
    # Handle payment externally
    tx_signature = await your_payment_function(
        recipient=e.recipient,
        amount=e.amount,
        memo=e.memo
    )
    
    # Retry with payment proof
    result = await client._request(
        "POST",
        "/analyze",
        json={"market": "..."},
        headers={"X-Payment-Tx": tx_signature}
    )
```

---

## Direct HTTP (No SDK)

You can also use the API directly:

### Step 1: Initial Request

```bash
curl -X POST https://api.nodo.ai/x402/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"market": "polymarket.com/event/btc-150k", "tier": "deep"}'
```

### Step 2: Parse 402 Response

```json
{
  "payment": {
    "amount": "0.10",
    "recipient": "NoDo...",
    "memo": "req_abc123"
  }
}
```

### Step 3: Send USDC Payment

Use any Solana wallet/library to send USDC.

### Step 4: Retry with Proof

```bash
curl -X POST https://api.nodo.ai/x402/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-Payment-Tx: YOUR_TX_SIGNATURE" \
  -d '{"market": "polymarket.com/event/btc-150k", "tier": "deep"}'
```

---

## Webhooks Integration

```python
# Create webhook for alerts
webhook = await client.create_webhook(
    url="https://yoursite.com/nodo-webhook",
    events=[
        "opportunity.yield",
        "opportunity.delta",
    ],
    filters={
        "min_profit": 5.0,
        "topics": ["BTC", "ETH"]
    }
)

print(f"Webhook ID: {webhook['id']}")
```

**Webhook Payload:**
```json
{
  "event": "opportunity.yield",
  "data": {
    "question": "Will BTC hit $200K?",
    "outcome": "NO",
    "profit_pct": 5.2,
    "apy": 120,
    "url": "https://polymarket.com/..."
  },
  "timestamp": "2025-01-01T12:00:00Z"
}
```

---

## Error Handling

```python
from nodo_x402 import (
    NodoClient,
    PaymentRequired,
    PaymentFailed,
    APIError,
    WalletError
)

client = NodoClient(keypair_path="~/.config/solana/id.json")

try:
    result = await client.analyze(market="...")
    
except PaymentRequired as e:
    # 402 - Payment needed (only if auto_pay=False)
    print(f"Need to pay: ${e.amount}")
    
except PaymentFailed as e:
    # Payment transaction failed
    print(f"Payment failed: {e}")
    
except APIError as e:
    # API returned error
    print(f"API error {e.status_code}: {e.message}")
    
except WalletError as e:
    # Wallet/key issues
    print(f"Wallet error: {e}")
```

---

## Best Practices

### 1. Reuse Client Instance

```python
# Good - reuse client
client = NodoClient(...)
result1 = await client.analyze(...)
result2 = await client.analyze(...)
await client.close()

# Bad - creating new client each time
result1 = await NodoClient(...).analyze(...)
result2 = await NodoClient(...).analyze(...)
```

### 2. Use Context Manager

```python
async with NodoClient(keypair_path="...") as client:
    result = await client.analyze(...)
# Automatically closes
```

### 3. Batch Requests When Possible

```python
# Scan once, analyze interesting ones
opportunities = await client.yield_scan(limit=50)

# Filter locally first
interesting = [o for o in opportunities if o.apy > 100]

# Then do paid analysis only on best ones
for opp in interesting[:3]:
    analysis = await client.analyze(market=opp.url, tier="deep")
```

### 4. Cache Results

```python
import hashlib
from functools import lru_cache

@lru_cache(maxsize=100)
async def cached_analyze(market_url: str, tier: str):
    return await client.analyze(market=market_url, tier=tier)
```

