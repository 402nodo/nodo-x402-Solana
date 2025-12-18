# 🏗️ Architecture

## System Overview

NODO x402 Protocol consists of 4 main components:

```
┌──────────────────────────────────────────────────────────────┐
│                    NODO x402 System                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │   Client     │  ← Users/AI Agents                        │
│  │   (SDK)      │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         │ HTTP Request                                       │
│         │                                                    │
│  ┌──────▼────────────────────────────────────────────────┐  │
│  │              FastAPI Server                           │  │
│  │  ┌─────────────────────────────────────────────┐     │  │
│  │  │         x402 Middleware                     │     │  │
│  │  │  • Check payment header                     │     │  │
│  │  │  • Return 402 if none                       │     │  │
│  │  │  • Verify if present                        │     │  │
│  │  └────────────┬────────────────────────────────┘     │  │
│  │               │                                       │  │
│  │  ┌────────────▼────────────────────────────────┐     │  │
│  │  │         Solana Payment Client               │     │  │
│  │  │  • Connect to Solana RPC                    │     │  │
│  │  │  • Verify USDC transfers                    │     │  │
│  │  │  • Replay protection                        │     │  │
│  │  └────────────┬────────────────────────────────┘     │  │
│  │               │                                       │  │
│  │  ┌────────────▼────────────────────────────────┐     │  │
│  │  │         API Endpoints                       │     │  │
│  │  │  • /analyze (AI analysis)                   │     │  │
│  │  │  • /yield/scan (opportunities)              │     │  │
│  │  │  • /delta/scan (mispricing)                 │     │  │
│  │  │  • /markets (data)                          │     │  │
│  │  └─────────────────────────────────────────────┘     │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                   │
│                          │ Solana RPC                        │
│                          ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Solana Blockchain                       │  │
│  │  • Verify transactions                               │  │
│  │  • Check USDC transfers                              │  │
│  │  • 400ms finality                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Client (SDK)

**Location**: `sdk/python/`, `sdk/typescript/`

**Responsibility**: Handle x402 payment flow automatically

**Key Features**:
- Detect 402 responses
- Send USDC on Solana
- Retry with payment proof
- Wallet management

**Flow**:
```python
# User code
result = await client.analyze(market="...")

# SDK handles internally:
# 1. Make request → Get 402
# 2. Parse payment details
# 3. Send USDC on Solana
# 4. Retry with X-Payment-Tx header
# 5. Return result
```

### 2. x402 Middleware

**Location**: `src/middleware/x402.py`

**Responsibility**: Intercept requests and enforce payment

**Algorithm**:
```python
def process_request(request):
    # 1. Check if endpoint requires payment
    if endpoint not in PAID_ENDPOINTS:
        return proceed()
    
    # 2. Check for payment proof header
    tx_signature = request.headers.get("X-Payment-Tx")
    if not tx_signature:
        return return_402()
    
    # 3. Verify payment
    if verify_payment(tx_signature, expected_amount):
        return proceed()
    else:
        return return_402_invalid()
```

**Paid Endpoints**:
```python
PAID_ENDPOINTS = {
    "/analyze": lambda r: get_price("analyze", r.query_params.get("tier")),
    "/yield/scan": lambda r: 0.005,
    "/delta/scan": lambda r: 0.01,
    "/smart/analyze": lambda r: 0.02,
    "/arbitrage/scan": lambda r: 0.01,
    "/markets": lambda r: 0.001,
    "/webhooks": lambda r: 0.005,
}
```

**Free Endpoints**:
```python
FREE_ENDPOINTS = {
    "/",
    "/docs",
    "/health",
    "/x402/info",
    "/account/balance",
    "/account/usage",
}
```

### 3. Solana Payment Client

**Location**: `src/solana/client.py`

**Responsibility**: Verify USDC payments on Solana blockchain

**Verification Checklist**:
```python
async def verify_usdc_transfer(tx_signature, expected_amount):
    # 1. Get transaction from Solana
    tx = await client.get_transaction(signature)
    
    if not tx:
        return {"valid": False, "error": "Transaction not found"}
    
    # 2. Check transaction succeeded
    if tx.meta.err:
        return {"valid": False, "error": "Transaction failed"}
    
    # 3. Check transaction age
    if tx.block_time and (now() - tx.block_time) > 300:
        return {"valid": False, "error": "Transaction too old"}
    
    # 4. Parse SPL token transfer
    transfer = parse_token_transfer(tx, USDC_MINT)
    if not transfer:
        return {"valid": False, "error": "No USDC transfer found"}
    
    # 5. Verify amount
    if abs(transfer.amount - expected_amount) > 0.000001:
        return {"valid": False, "error": "Amount mismatch"}
    
    # 6. Verify recipient
    if transfer.recipient != NODO_WALLET:
        return {"valid": False, "error": "Wrong recipient"}
    
    # 7. Check replay (not used before)
    if is_signature_used(tx_signature):
        return {"valid": False, "error": "Payment already used"}
    
    # 8. Mark as used
    mark_signature_used(tx_signature)
    
    return {"valid": True, "amount": transfer.amount}
```

**Replay Protection**:
```python
# In-memory cache (production should use Redis)
used_signatures = set()

def is_signature_used(sig):
    return sig in used_signatures

def mark_signature_used(sig):
    used_signatures.add(sig)
    # Also save to database for persistence
```

### 4. API Endpoints

**Location**: `src/api/`

**Responsibility**: Business logic for each service

**Example - AI Analysis**:
```python
@router.post("/analyze")
async def analyze_market(request: AnalyzeRequest):
    # Middleware already verified payment
    # Just process the request
    
    # 1. Fetch market data
    market = await fetch_market(request.market)
    
    # 2. Run AI analysis
    models = select_models(request.tier)  # 1, 3, or 6
    tasks = [model.analyze(market) for model in models]
    results = await asyncio.gather(*tasks)
    
    # 3. Build consensus
    consensus = aggregate_results(results)
    
    # 4. Return response
    return {
        "analysis": consensus,
        "models": results,
        "meta": {
            "cost": f"${get_price(request.tier)}",
            "tier": request.tier
        }
    }
```

---

## Data Flow

### Complete Request Lifecycle

```
1. CLIENT INITIATES
   ├─ client.analyze(market="...", tier="deep")
   └─ SDK makes HTTP request

2. SERVER RECEIVES
   ├─ FastAPI receives POST /analyze
   └─ x402 Middleware intercepts

3. PAYMENT CHECK
   ├─ No X-Payment-Tx header found
   └─ Return 402 Payment Required

4. CLIENT GETS 402
   ├─ SDK parses payment details
   ├─ amount: 0.10
   ├─ recipient: NoDo...
   └─ memo: req_abc123

5. CLIENT PAYS
   ├─ Load Solana wallet
   ├─ Build USDC transfer transaction
   ├─ Sign with private key
   ├─ Send to Solana network
   └─ Get tx_signature: 5K7mN...

6. SOLANA PROCESSES
   ├─ Validate transaction
   ├─ Execute USDC transfer
   ├─ Finalize in ~400ms
   └─ Tx confirmed

7. CLIENT RETRIES
   ├─ Same request
   └─ + header: X-Payment-Tx: 5K7mN...

8. SERVER VERIFIES
   ├─ x402 Middleware sees header
   ├─ Call Solana RPC
   ├─ Verify transaction on-chain
   ├─ Check amount, recipient, age
   └─ ✅ Payment valid

9. SERVER PROCESSES
   ├─ Middleware allows request
   ├─ Route to /analyze endpoint
   ├─ Run AI analysis (6 models)
   └─ Build response

10. CLIENT RECEIVES
    ├─ 200 OK
    ├─ {analysis: {...}, models: [...]}
    └─ meta: {cost: "$0.10", tx_signature: "5K7mN..."}
```

---

## Security Architecture

### 1. Payment Verification

**Multiple Layers**:
```
Layer 1: Transaction Exists
├─ Query Solana RPC
└─ Reject if not found

Layer 2: Transaction Succeeded
├─ Check tx.meta.err
└─ Reject if failed

Layer 3: Amount Verification
├─ Parse token transfer instruction
├─ Extract amount
└─ Reject if mismatch (±0.000001 tolerance)

Layer 4: Recipient Verification
├─ Check transfer destination
└─ Reject if not our wallet

Layer 5: Replay Protection
├─ Check if signature used before
├─ Store in Redis/DB
└─ Reject if duplicate

Layer 6: Age Check
├─ Check block timestamp
└─ Reject if >5 minutes old
```

### 2. Rate Limiting

**Per-Wallet Limits**:
```python
RATE_LIMITS = {
    "default": "60/minute",
    "paid_user": "600/minute",
    "enterprise": "unlimited"
}

# In middleware
@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    wallet = get_wallet_from_request(request)
    
    if is_rate_limited(wallet):
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded"}
        )
    
    return await call_next(request)
```

### 3. Input Validation

**Strict Validation**:
```python
class AnalyzeRequest(BaseModel):
    market: str = Field(..., min_length=10, max_length=200)
    tier: str = Field(default="standard", regex="^(quick|standard|deep)$")
    strategy: str = Field(default="yield_farming", regex="^(yield_farming|delta_neutral|momentum)$")
```

---

## Performance Optimizations

### 1. Parallel AI Requests

```python
# Instead of sequential (slow)
result1 = await claude.analyze(market)
result2 = await gpt4.analyze(market)
result3 = await gemini.analyze(market)
# Total: 6-9 seconds

# Use parallel (fast)
results = await asyncio.gather(
    claude.analyze(market),
    gpt4.analyze(market),
    gemini.analyze(market)
)
# Total: 2-3 seconds (fastest model)
```

### 2. Connection Pooling

```python
# Reuse HTTP connections
client = httpx.AsyncClient(
    timeout=60.0,
    limits=httpx.Limits(max_keepalive_connections=20)
)

# Reuse Solana RPC connection
solana_client = AsyncClient(
    rpc_url,
    timeout=30.0,
    commitment="confirmed"
)
```

### 3. Response Caching

```python
# Cache market data for 1 minute
@lru_cache(maxsize=1000)
def get_market_data(market_id):
    return fetch_from_polymarket(market_id)
```

### 4. Database Indexing

```sql
-- Index for fast replay protection lookup
CREATE INDEX idx_used_signatures 
ON used_payments (tx_signature);

-- Index for user usage stats
CREATE INDEX idx_user_payments 
ON payments (user_wallet, created_at DESC);
```

---

## Scalability

### Horizontal Scaling

```
┌─────────────┐
│   Clients   │
└──────┬──────┘
       │
┌──────▼──────────┐
│  Load Balancer  │
└──────┬──────────┘
       │
   ┌───┴───┬───┬───┐
   │       │   │   │
┌──▼──┐ ┌─▼─┐ │ ┌─▼─┐
│API 1│ │...│ │ │N  │
└──┬──┘ └───┘ │ └───┘
   │          │
┌──▼──────────▼────┐
│  Redis (shared)  │
│  - Rate limits   │
│  - Replay cache  │
└──────────────────┘
   │
┌──▼──────────────┐
│   PostgreSQL    │
│  - Payments     │
│  - Usage stats  │
└─────────────────┘
```

### Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| Request latency | <100ms | 45ms (p50) |
| Payment verification | <500ms | 450ms (p50) |
| Throughput | 1000 req/s | 850 req/s |
| Uptime | 99.9% | 99.95% |

---

## Monitoring

### Key Metrics

**Payment Metrics**:
- Total payments/hour
- Payment success rate
- Average payment time
- Failed verifications (with reasons)

**API Metrics**:
- Requests/second per endpoint
- Response time per endpoint
- Error rate
- 402 responses vs successful

**Solana Metrics**:
- RPC latency
- Transaction confirmation time
- Failed transactions

**Business Metrics**:
- Revenue/hour
- Active users
- Popular endpoints
- Geographic distribution

### Alerts

```yaml
alerts:
  - name: Payment verification slow
    condition: payment_verification_p95 > 2000ms
    action: page_oncall
  
  - name: High error rate
    condition: error_rate > 5%
    action: send_slack
  
  - name: Solana RPC down
    condition: solana_rpc_errors > 10
    action: failover_rpc
```

---

## Deployment Architecture

### Production Setup

```
┌──────────────────────────────────────────┐
│           Cloudflare CDN                  │
│  • DDoS protection                        │
│  • SSL termination                        │
│  • Geographic routing                     │
└──────────────────┬───────────────────────┘
                   │
┌──────────────────▼───────────────────────┐
│         Application Servers               │
│  • Railway / Fly.io / AWS                │
│  • Auto-scaling (2-10 instances)         │
│  • Health checks                         │
└──────────────────┬───────────────────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
┌─────▼────┐ ┌────▼───┐ ┌─────▼────┐
│ Redis    │ │Postgres│ │  Solana  │
│ (Upstash)│ │(Neon)  │ │   RPC    │
└──────────┘ └────────┘ └──────────┘
```

---

[Next: Payment Flow →](payment-flow.md)
