# 📦 SDK Guide

## Overview

NODO x402 provides official SDKs for Python and TypeScript with automatic payment handling.

---

## Python SDK

### Installation

```bash
# Basic installation
pip install nodo-x402

# With Solana support (recommended)
pip install nodo-x402[solana]
```

### Initialization

```python
from nodo_x402 import NodoClient

# Option 1: From keypair file
client = NodoClient(
    keypair_path="~/.config/solana/id.json"
)

# Option 2: From private key bytes
client = NodoClient(
    private_key=your_private_key_bytes
)

# Option 3: Manual payment mode
client = NodoClient(
    keypair_path="~/.config/solana/id.json",
    auto_pay=False  # Handle payments yourself
)

# Option 4: Custom RPC
client = NodoClient(
    keypair_path="~/.config/solana/id.json",
    rpc_url="https://your-rpc.com"
)
```

### Methods

#### analyze()

```python
result = await client.analyze(
    market="polymarket.com/event/btc-150k",
    tier="deep",           # quick, standard, deep
    strategy="yield_farming"  # yield_farming, delta_neutral, momentum
)

# Result structure
result.consensus        # "BUY_NO"
result.agreement        # "5/6"
result.confidence       # 82
result.models           # List[AIModelResult]
result.dissent          # Optional dissenting opinion
result.risks            # List[str]
result.market_question  # "Will Bitcoin reach..."
result.cost             # "$0.10"
```

#### yield_scan()

```python
opportunities = await client.yield_scan(
    min_probability=0.95,
    min_volume=10000,
    max_days=30,
    risk_level="LOW",  # LOW, MEDIUM, HIGH
    limit=20
)

for opp in opportunities:
    opp.question           # Market question
    opp.outcome            # "YES" or "NO"
    opp.buy_price          # 0.97
    opp.profit_pct         # 3.09
    opp.apy                # 112.8
    opp.days_to_resolution # 10
    opp.risk_level         # "LOW"
```

#### delta_scan()

```python
deltas = await client.delta_scan(
    min_profit=5.0,
    min_confidence=50,
    topic="BTC",  # BTC, ETH, TRUMP, etc
    limit=20
)

for d in deltas:
    d.topic              # "BTC"
    d.logic_error        # Description of mispricing
    d.profit_potential   # 33.3
    d.confidence         # 90
    d.action             # "BUY '$100K' YES"
    d.event_a            # First market
    d.event_b            # Second market
```

#### smart_analyze()

```python
result = await client.smart_analyze(
    question="Will Bitcoin reach $200K?",
    current_price=0.15,
    outcome="NO",
    days_left=14
)

# Returns dict with:
# category, confidence_score, verdict, reasons, risks, data_used
```

#### get_markets()

```python
markets = await client.get_markets(
    platform="polymarket",  # polymarket, kalshi
    min_volume=10000,
    search="bitcoin",
    limit=50
)

for m in markets:
    m.id
    m.question
    m.yes_price
    m.no_price
    m.volume
    m.url
```

#### Webhooks

```python
# Create
webhook = await client.create_webhook(
    url="https://yoursite.com/webhook",
    events=["opportunity.yield", "opportunity.delta"],
    filters={"min_profit": 5.0}
)

# List
webhooks = await client.list_webhooks()

# Delete
await client.delete_webhook(webhook_id)
```

#### Account

```python
# Get usage stats
usage = await client.get_usage(period="2025-01")

# Get pricing
pricing = await client.get_pricing()
```

### Models

```python
from nodo_x402 import (
    AnalysisResult,
    YieldOpportunity,
    DeltaOpportunity,
    Market,
    AIModelResult,
)
```

### Exceptions

```python
from nodo_x402 import (
    NodoError,         # Base exception
    PaymentRequired,   # 402 - need payment
    PaymentFailed,     # Payment tx failed
    APIError,          # API returned error
    WalletError,       # Wallet issues
    InsufficientFunds, # Not enough USDC
)
```

---

## TypeScript SDK

### Installation

```bash
npm install @nodo-ai/x402
# or
yarn add @nodo-ai/x402
```

### Initialization

```typescript
import { NodoClient } from '@nodo-ai/x402';
import { Keypair } from '@solana/web3.js';

// Option 1: From keypair
const keypair = Keypair.fromSecretKey(secretKeyBytes);
const client = new NodoClient({
  keypair: keypair.secretKey,
});

// Option 2: Manual payment mode
const client = new NodoClient({
  keypair: keypair.secretKey,
  autoPay: false,
});

// Option 3: Custom settings
const client = new NodoClient({
  keypair: keypair.secretKey,
  baseUrl: 'https://api.nodo.ai/x402/v1',
  rpcUrl: 'https://your-rpc.com',
});
```

### Methods

#### analyze()

```typescript
const result = await client.analyze({
  market: 'polymarket.com/event/btc-150k',
  tier: 'deep',
  strategy: 'yield_farming',
});

// Result structure
result.analysis.consensus   // "BUY_NO"
result.analysis.agreement   // "5/6"
result.analysis.confidence  // 82
result.models               // AIModelResult[]
result.dissent              // Dissent | undefined
result.risks                // string[]
result.meta.cost            // "$0.10"
```

#### yieldScan()

```typescript
const opportunities = await client.yieldScan({
  minProbability: 0.95,
  minVolume: 10000,
  maxDays: 30,
  riskLevel: 'LOW',
  limit: 20,
});

for (const opp of opportunities) {
  console.log(opp.question);
  console.log(opp.outcome);     // "YES" | "NO"
  console.log(opp.buyPrice);    // 0.97
  console.log(opp.profitPct);   // 3.09
  console.log(opp.apy);         // 112.8
}
```

#### deltaScan()

```typescript
const deltas = await client.deltaScan({
  minProfit: 5.0,
  minConfidence: 50,
  topic: 'BTC',
  limit: 20,
});

for (const d of deltas) {
  console.log(d.topic);
  console.log(d.logicError);
  console.log(d.profitPotential);
  console.log(d.action);
}
```

#### smartAnalyze()

```typescript
const result = await client.smartAnalyze({
  question: 'Will Bitcoin reach $200K?',
  currentPrice: 0.15,
  outcome: 'NO',
  daysLeft: 14,
});
```

#### getMarkets()

```typescript
const markets = await client.getMarkets({
  platform: 'polymarket',
  minVolume: 10000,
  search: 'bitcoin',
  limit: 50,
});

for (const m of markets) {
  console.log(m.question);
  console.log(m.yesPrice);
  console.log(m.noPrice);
}
```

#### Webhooks

```typescript
// Create
const webhook = await client.createWebhook({
  url: 'https://yoursite.com/webhook',
  events: ['opportunity.yield'],
});

// List
const webhooks = await client.listWebhooks();

// Delete
await client.deleteWebhook(webhookId);
```

### Types

```typescript
import type {
  AnalysisResult,
  YieldOpportunity,
  DeltaOpportunity,
  Market,
  AIModelResult,
  Dissent,
  Webhook,
  UsageStats,
  NodoClientOptions,
  AnalyzeOptions,
  YieldScanOptions,
  DeltaScanOptions,
  MarketsOptions,
} from '@nodo-ai/x402';
```

### Errors

```typescript
import {
  NodoError,
  PaymentRequired,
  PaymentFailed,
  APIError,
  WalletError,
  InsufficientFunds,
} from '@nodo-ai/x402';

try {
  const result = await client.analyze({ market: '...' });
} catch (error) {
  if (error instanceof PaymentRequired) {
    console.log(`Need: $${error.amount}`);
    console.log(`Send to: ${error.recipient}`);
  } else if (error instanceof APIError) {
    console.log(`API error ${error.statusCode}`);
  }
}
```

---

## Comparison

| Feature | Python | TypeScript |
|---------|--------|------------|
| Auto-payment | ✅ | ✅ |
| Async/await | ✅ | ✅ |
| Type hints | ✅ | ✅ |
| Solana integration | ✅ | ✅ |
| Context manager | ✅ | ❌ |
| Package manager | pip | npm/yarn |

