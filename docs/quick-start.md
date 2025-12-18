# 🚀 Quick Start

Get started with x402 in 5 minutes.

---

## For API Consumers

### 1. Install SDK

**Python:**
```bash
pip install nodo-x402
```

**TypeScript:**
```bash
npm install @nodo-ai/x402
```

### 2. Get Solana Wallet

You need a Solana wallet with USDC:

**Option A: Use Phantom**
1. Install [Phantom](https://phantom.app/)
2. Create wallet
3. Buy USDC on Phantom (card/Apple Pay)
4. Export private key: Settings → Export Private Key

**Option B: Use CLI**
```bash
# Install Solana CLI
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"

# Generate keypair
solana-keygen new --outfile ~/.config/solana/id.json

# Get your address
solana address

# Airdrop SOL (devnet only)
solana airdrop 1

# Buy USDC on mainnet at phantom.app
```

### 3. Make Your First Request

**Python:**
```python
from nodo_x402 import NodoClient
import asyncio

async def main():
    # Initialize client
    client = NodoClient(
        keypair_path="~/.config/solana/id.json"
    )
    
    # Make request - payment happens automatically
    result = await client.analyze(
        market="polymarket.com/event/btc-150k-2025",
        tier="quick"  # $0.01
    )
    
    print(f"Consensus: {result.consensus}")
    print(f"Confidence: {result.confidence}%")
    print(f"Cost: {result.cost}")
    
    await client.close()

asyncio.run(main())
```

**TypeScript:**
```typescript
import { NodoClient } from '@nodo-ai/x402';
import { Keypair } from '@solana/web3.js';
import fs from 'fs';

async function main() {
  // Load keypair
  const keypairFile = fs.readFileSync(
    process.env.HOME + '/.config/solana/id.json'
  );
  const keypair = Keypair.fromSecretKey(
    Uint8Array.from(JSON.parse(keypairFile.toString()))
  );
  
  // Initialize client
  const client = new NodoClient({ 
    keypair: keypair.secretKey 
  });
  
  // Make request - payment happens automatically
  const result = await client.analyze({
    market: 'polymarket.com/event/btc-150k-2025',
    tier: 'quick'  // $0.01
  });
  
  console.log(`Consensus: ${result.analysis.consensus}`);
  console.log(`Confidence: ${result.analysis.confidence}%`);
  console.log(`Cost: ${result.meta.cost}`);
}

main();
```

**Output:**
```
Consensus: BUY_NO
Confidence: 82%
Cost: $0.01
```

✅ Payment of $0.01 USDC was sent automatically!

---

## For API Providers

Want to add x402 to your API?

### 1. Install Dependencies

```bash
pip install fastapi uvicorn solana solders spl-token
```

### 2. Create Minimal x402 Server

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uuid
from datetime import datetime, timedelta, timezone

app = FastAPI()

# Your Solana wallet address (receives payments)
WALLET_ADDRESS = "YOUR_SOLANA_ADDRESS_HERE"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

@app.middleware("http")
async def x402_middleware(request: Request, call_next):
    # Skip payment for health checks
    if request.url.path == "/health":
        return await call_next(request)
    
    # Check for payment proof
    tx_signature = request.headers.get("X-Payment-Tx")
    
    if not tx_signature:
        # Return 402 Payment Required
        request_id = f"req_{uuid.uuid4().hex[:12]}"
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
        
        return JSONResponse(
            status_code=402,
            content={
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
                    "recipient": WALLET_ADDRESS,
                    "usdc_mint": USDC_MINT,
                    "memo": request_id,
                    "expires_at": expires_at.isoformat()
                }
            }
        )
    
    # TODO: Verify payment on Solana (see next step)
    # For now, trust the signature (DON'T DO THIS IN PRODUCTION!)
    
    return await call_next(request)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/data")
async def get_data():
    # This endpoint requires payment
    return {"data": "valuable information"}
```

### 3. Add Payment Verification

```python
from solana.rpc.async_api import AsyncClient
from solders.signature import Signature

async def verify_payment(tx_signature: str, expected_amount: float):
    """Verify USDC payment on Solana."""
    client = AsyncClient("https://api.mainnet-beta.solana.com")
    
    try:
        # Get transaction
        sig = Signature.from_string(tx_signature)
        tx = await client.get_transaction(
            sig,
            encoding="jsonParsed",
            max_supported_transaction_version=0
        )
        
        if not tx.value:
            return False
        
        # Check transaction succeeded
        if tx.value.transaction.meta.err:
            return False
        
        # Parse SPL token transfers
        for ix in tx.value.transaction.transaction.message.instructions:
            if hasattr(ix, 'parsed'):
                parsed = ix.parsed
                if parsed.get('type') == 'transferChecked':
                    info = parsed.get('info', {})
                    
                    # Check amount
                    amount = float(info.get('tokenAmount', {}).get('uiAmount', 0))
                    if abs(amount - expected_amount) < 0.000001:
                        # Check recipient
                        # (You should also verify the destination matches your wallet)
                        return True
        
        return False
        
    except Exception as e:
        print(f"Verification error: {e}")
        return False

# Update middleware
@app.middleware("http")
async def x402_middleware(request: Request, call_next):
    if request.url.path == "/health":
        return await call_next(request)
    
    tx_signature = request.headers.get("X-Payment-Tx")
    
    if not tx_signature:
        # Return 402 (same as before)
        ...
    
    # Verify payment
    if await verify_payment(tx_signature, 0.10):
        return await call_next(request)
    
    return JSONResponse(
        status_code=402,
        content={"error": "Invalid payment"}
    )
```

### 4. Run Server

```bash
uvicorn main:app --reload
```

Test it:
```bash
# No payment - get 402
curl http://localhost:8000/api/data

# With payment - get data
curl -H "X-Payment-Tx: YourSolanaTransactionSignature" \
     http://localhost:8000/api/data
```

---

## Testing on Devnet

For development, use Solana devnet:

### 1. Switch to Devnet

```python
# In your code
client = NodoClient(
    keypair_path="~/.config/solana/id.json",
    base_url="http://localhost:8000",  # Your test server
    rpc_url="https://api.devnet.solana.com"  # Devnet
)
```

### 2. Get Devnet SOL and USDC

```bash
# Get devnet SOL (for fees)
solana airdrop 1 --url devnet

# Get devnet USDC
# Visit: https://spl-token-faucet.com
# Request devnet USDC to your address
```

### 3. Test Without Real Money

```bash
# Your test server returns 402
# SDK sends devnet USDC
# Server verifies on devnet
# ✅ No real money spent
```

---

## Common Patterns

### Pattern 1: Batch Requests

```python
markets = [
    "polymarket.com/event/btc-150k",
    "polymarket.com/event/eth-10k",
    "polymarket.com/event/sol-500"
]

# Sequential (3 payments)
for market in markets:
    result = await client.analyze(market, tier="quick")
    print(result.consensus)

# Parallel (3 payments at once)
import asyncio
tasks = [
    client.analyze(market, tier="quick")
    for market in markets
]
results = await asyncio.gather(*tasks)
```

### Pattern 2: Budget Control

```python
class BudgetClient:
    def __init__(self, client, daily_budget):
        self.client = client
        self.daily_budget = daily_budget
        self.spent_today = 0
    
    async def analyze(self, market, tier="quick"):
        price = {"quick": 0.01, "standard": 0.05, "deep": 0.10}[tier]
        
        if self.spent_today + price > self.daily_budget:
            raise Exception("Daily budget exceeded")
        
        result = await self.client.analyze(market, tier=tier)
        self.spent_today += price
        return result

# Use it
budget_client = BudgetClient(client, daily_budget=1.00)
result = await budget_client.analyze(market, tier="deep")
```

### Pattern 3: Caching

```python
import hashlib
import json

cache = {}

async def cached_analyze(client, market, tier="quick"):
    # Cache key
    key = hashlib.md5(f"{market}{tier}".encode()).hexdigest()
    
    # Check cache
    if key in cache:
        print("Using cached result (no payment)")
        return cache[key]
    
    # Make request (pays)
    result = await client.analyze(market, tier=tier)
    
    # Cache for 5 minutes
    cache[key] = result
    return result
```

---

## Next Steps

### Learn More
- [Architecture](architecture.md) - How x402 works internally
- [Payment Flow](payment-flow.md) - Detailed payment process
- [API Reference](api.md) - Full API documentation

### Build
- [Middleware Setup](middleware-setup.md) - Integrate x402 into your API
- [Solana Verification](solana-verification.md) - Verify payments correctly
- [Custom Pricing](custom-pricing.md) - Set your own prices

### Examples
- [Python Examples](../examples/python/) - Complete examples
- [TypeScript Examples](../examples/typescript/) - Complete examples
- [Use Cases](../examples/use-cases.md) - Real-world patterns

---

## Support

Need help?

- 📧 **Email**: dev@nodo.ai
- 💬 **Discord**: [Join server](https://discord.gg/nodo)
- 🐛 **Issues**: [GitHub](https://github.com/nodo-ai/nodo-x402-protocol/issues)
- 📚 **Docs**: [Full documentation](README.md)

---

[Next: Architecture →](architecture.md)

