# 💳 What is x402?

## Overview

**x402** is Solana's implementation of **HTTP 402 Payment Required** - a status code that has existed since 1997 but was never widely adopted until now.

The x402 protocol enables micropayments for API requests, making pay-per-use business models economically viable.

---

## The HTTP 402 Status Code

From [RFC 7231](https://tools.ietf.org/html/rfc7231#section-6.5.2):

> **402 Payment Required**
>
> The 402 (Payment Required) status code is reserved for future use.

This status code was created for the web of the future - a web where content and services could be monetized with micropayments. But it never took off because:

1. **High transaction fees** - Credit card fees ($0.30+) made micropayments impossible
2. **Slow settlement** - Bank transfers take days
3. **No global standard** - Each payment system was different
4. **Complex integration** - Payment processing was difficult

---

## Enter Solana

Solana makes x402 finally practical:

```
┌─────────────────────────────────────────────────────┐
│                 Solana Advantages                    │
├─────────────────────────────────────────────────────┤
│ • Finality: 400ms (vs 3-5 days for banks)          │
│ • Fees: $0.00025 (vs $0.30+ for cards)             │
│ • Minimum: $0.001 (vs $1-10 for Stripe)            │
│ • Global: No geographic restrictions                │
│ • Programmable: Smart contracts, tokens, DeFi       │
│ • AI Ready: Agents can pay autonomously             │
└─────────────────────────────────────────────────────┘
```

---

## How x402 Works

### Traditional API (Subscription)

```
User → Sign up → Add credit card → Monthly charge → API access
       ⏱️ 10 min setup    💳 $10-100/month    📊 Pay for unused calls
```

### x402 API (Pay-per-request)

```
User → Make request → 402 Payment Required → Pay $0.01 → Get response
       ⚡ Instant          💰 Exact cost         ⏱️ 400ms payment
```

---

## Real-World Example

### NODO AI Analysis API

**Before x402 (Traditional):**
```
Monthly Plans:
- Basic: $50/month (100 requests)
- Pro: $200/month (1000 requests)
- Enterprise: $1000+/month (Unlimited)

Problems:
❌ Pay for unused requests
❌ High commitment
❌ Not accessible to hobbyists
❌ Can't start with 1 request
```

**With x402 (Pay-per-request):**
```
Pricing:
- Quick Analysis: $0.01/request
- Standard Analysis: $0.05/request
- Deep Analysis: $0.10/request

Benefits:
✅ Pay only for what you use
✅ Start with $0.01
✅ Scale from 1 to 1M requests
✅ Perfect for AI agents
```

---

## x402 Response Format

When you make a request without payment:

```http
HTTP/1.1 402 Payment Required
Content-Type: application/json

{
  "error": {
    "code": "PAYMENT_REQUIRED",
    "message": "This request requires payment of $0.10 USDC"
  },
  "payment": {
    "x402_version": 1,
    "network": "solana-mainnet",
    "amount": "0.100000",
    "currency": "USDC",
    "decimals": 6,
    "recipient": "NoDo7nX4t2QGKDC7B9a3qRhCmj8K8vM9HwxAJpKgZrMw",
    "usdc_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "memo": "req_abc123",
    "expires_at": "2025-12-19T12:05:00Z"
  }
}
```

The client then:
1. Sends USDC on Solana (400ms)
2. Retries request with transaction signature
3. Gets the actual API response

---

## Use Cases

### 1. AI APIs

```python
# Instead of $200/month subscription
# Pay $0.10 per AI analysis

result = await client.analyze(market="...", tier="deep")
# ✅ Paid $0.10, got result
```

### 2. Data APIs

```python
# Instead of $1000/month for unlimited data
# Pay $0.001 per market data request

market = await client.get_market("btc-150k")
# ✅ Paid $0.001, got data
```

### 3. AI Agents

```python
# AI agent can pay autonomously
# No human approval needed

agent_wallet = load_wallet("agent_keypair.json")
client = NodoClient(keypair=agent_wallet)

# Agent loops 24/7
while True:
    opportunities = await client.yield_scan()  # $0.005
    for opp in opportunities:
        analysis = await client.analyze(opp.market)  # $0.05
        if analysis.consensus == "BUY":
            execute_trade(opp)
```

### 4. Webhooks/Alerts

```python
# Pay only for alerts you receive
# Not a fixed monthly fee

webhook = await client.create_webhook(
    url="https://myapp.com/webhook",
    events=["opportunity.yield"]
)
# ✅ $0.005 per alert sent
```

---

## Comparison with Alternatives

| Method | Min Payment | Fee | Finality | Global | AI Agent Ready |
|--------|-------------|-----|----------|--------|----------------|
| **x402 Solana** | $0.001 | $0.00025 | 400ms | ✅ | ✅ |
| Stripe | $1.00 | $0.30 + 2.9% | 2-7 days | Limited | ❌ |
| PayPal | $0.01 | $0.39 + 3.4% | 1-3 days | Limited | ❌ |
| Lightning (BTC) | ~$0.01 | <$0.001 | ~1min | ✅ | ⚠️ |
| Ethereum | ~$1 | $1-50 | 12sec | ✅ | ⚠️ |

---

## Protocol Specification

### x402 Version 1

```typescript
interface X402Response {
  error: {
    code: "PAYMENT_REQUIRED";
    message: string;
  };
  payment: {
    x402_version: 1;
    network: "solana-mainnet" | "solana-devnet";
    amount: string;           // Decimal string, e.g. "0.100000"
    currency: "USDC" | "SOL"; // Token type
    decimals: number;         // Token decimals (6 for USDC)
    recipient: string;        // Solana address
    usdc_mint?: string;       // USDC mint address (if currency=USDC)
    memo?: string;            // Optional memo for tracking
    expires_at: string;       // ISO 8601 timestamp
  };
  request?: {
    id: string;
    endpoint: string;
    timestamp: string;
  };
}
```

### Payment Verification

Server MUST verify:
1. ✅ Transaction exists on Solana
2. ✅ Transaction succeeded (not failed)
3. ✅ Amount matches exactly (±0.000001 tolerance)
4. ✅ Recipient matches
5. ✅ Transaction timestamp within expiry
6. ✅ Transaction not used before (replay protection)

---

## Standards Compliance

x402 protocol follows:
- **HTTP RFC 7231** - HTTP 402 status code
- **Solana SPL Token** - Standard for USDC transfers
- **ISO 8601** - Timestamp format
- **Semantic Versioning** - x402_version field

---

## Ecosystem

### x402 Partners (40+)

- **Infrastructure**: Cloudflare, AWS, Anthropic
- **Wallets**: Phantom, Solflare, Backpack
- **Platforms**: Helius, Squads, Dialect
- **Market Cap**: $806M+

### Growing Adoption

```
x402 Transactions Growth:
Week 1:  5,000
Week 2:  15,000
Week 3:  50,000
Week 4:  500,000+ ⚡ 10,000% growth!
```

---

## Future Evolution

### x402 v2 (Planned)

- **Streaming payments**: Pay per second/byte
- **Conditional payments**: Pay only if condition met
- **Multi-token**: Accept multiple currencies
- **L402 compatibility**: Macaroons for delegation

---

## Learn More

- **Official Spec**: https://solana.com/x402
- **Our Implementation**: [Architecture →](architecture.md)
- **Try It**: [Quick Start →](quick-start.md)

---

[Next: Why Solana? →](why-solana.md)

