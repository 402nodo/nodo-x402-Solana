# 💳 Payment Flow

## x402 Protocol Flow

The x402 protocol implements HTTP 402 (Payment Required) on Solana. Here's exactly how payments work.

---

## Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                      x402 PAYMENT FLOW                            │
└──────────────────────────────────────────────────────────────────┘

┌──────────┐       ┌──────────────┐       ┌─────────────┐
│  Client  │       │  NODO API    │       │   Solana    │
│  (SDK)   │       │  Server      │       │   Network   │
└────┬─────┘       └──────┬───────┘       └──────┬──────┘
     │                    │                      │
     │  1. POST /analyze  │                      │
     │    (no payment)    │                      │
     │───────────────────>│                      │
     │                    │                      │
     │  2. 402 Payment    │                      │
     │     Required       │                      │
     │<───────────────────│                      │
     │                    │                      │
     │  Response:         │                      │
     │  {                 │                      │
     │    payment: {      │                      │
     │      amount: 0.10, │                      │
     │      recipient,    │                      │
     │      memo,         │                      │
     │      expires_at    │                      │
     │    }               │                      │
     │  }                 │                      │
     │                    │                      │
     │  3. USDC Transfer  │                      │
     │───────────────────────────────────────────>│
     │                    │                      │
     │  4. Tx Signature   │                      │
     │<──────────────────────────────────────────│
     │                    │                      │
     │  5. Retry request  │                      │
     │  + X-Payment-Tx    │                      │
     │───────────────────>│                      │
     │                    │                      │
     │                    │  6. Verify Tx        │
     │                    │─────────────────────>│
     │                    │                      │
     │                    │  7. Confirmation     │
     │                    │<─────────────────────│
     │                    │                      │
     │  8. 200 OK         │                      │
     │  + Analysis Result │                      │
     │<───────────────────│                      │
     │                    │                      │
```

---

## Step-by-Step

### Step 1: Initial Request

Client makes a request to a paid endpoint without payment:

```bash
curl -X POST https://api.nodo.ai/x402/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "market": "polymarket.com/event/btc-150k-2025",
    "tier": "deep"
  }'
```

### Step 2: 402 Response

Server returns HTTP 402 Payment Required:

```http
HTTP/1.1 402 Payment Required
X-Payment-Required: true
X-Payment-Amount: 0.10
X-Payment-Currency: USDC
X-Payment-Network: solana

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
    "memo": "req_a1b2c3d4e5f6",
    "expires_at": "2025-12-19T12:05:00Z",
    "instructions": {
      "description": "Send 0.10 USDC to recipient with memo",
      "steps": [
        "1. Send USDC SPL token transfer to recipient",
        "2. Include memo: req_a1b2c3d4e5f6",
        "3. Retry request with X-Payment-Tx header"
      ]
    }
  },
  "request": {
    "id": "req_a1b2c3d4e5f6",
    "endpoint": "/analyze",
    "method": "POST"
  }
}
```

### Step 3: Send Payment

Client creates and sends Solana USDC transfer:

```typescript
import { 
  Connection, 
  Transaction, 
  PublicKey 
} from '@solana/web3.js';
import { 
  createTransferCheckedInstruction,
  getAssociatedTokenAddress 
} from '@solana/spl-token';

// Setup
const connection = new Connection('https://api.mainnet-beta.solana.com');
const USDC_MINT = new PublicKey('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v');
const USDC_DECIMALS = 6;

// Get token accounts
const senderTokenAccount = await getAssociatedTokenAddress(
  USDC_MINT,
  senderPublicKey
);
const recipientTokenAccount = await getAssociatedTokenAddress(
  USDC_MINT,
  new PublicKey(payment.recipient)
);

// Build transaction
const tx = new Transaction();

// Add memo (optional but recommended)
tx.add(createMemoInstruction(payment.memo, [senderPublicKey]));

// Add USDC transfer
const amount = parseFloat(payment.amount) * Math.pow(10, USDC_DECIMALS);
tx.add(
  createTransferCheckedInstruction(
    senderTokenAccount,      // from
    USDC_MINT,               // mint
    recipientTokenAccount,   // to
    senderPublicKey,         // owner
    BigInt(amount),          // amount (0.10 * 10^6 = 100000)
    USDC_DECIMALS            // decimals
  )
);

// Send transaction
const signature = await connection.sendTransaction(tx, [keypair]);
await connection.confirmTransaction(signature);

console.log(`Payment sent: ${signature}`);
```

### Step 4: Get Signature

Transaction confirms on Solana (~400ms):

```
Transaction Signature: 5K7mNvuKR9vAqJNkqRV3f8WxYz...
```

### Step 5: Retry with Payment Proof

Client retries the original request with payment proof:

```bash
curl -X POST https://api.nodo.ai/x402/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-Payment-Tx: 5K7mNvuKR9vAqJNkqRV3f8WxYz..." \
  -d '{
    "market": "polymarket.com/event/btc-150k-2025",
    "tier": "deep"
  }'
```

### Step 6-7: Server Verifies Payment

Server checks transaction on Solana:

```python
async def verify_payment(tx_signature: str, expected_amount: float):
    # Fetch transaction
    tx = await solana_client.get_transaction(tx_signature)
    
    # Checks performed:
    # ✓ Transaction exists
    # ✓ Transaction succeeded (no errors)
    # ✓ Transfer is to correct recipient
    # ✓ Amount matches (± $0.000001 tolerance)
    # ✓ Currency is USDC
    # ✓ Transaction is recent (< 5 minutes)
    # ✓ Transaction not already used (replay protection)
    
    return {"valid": True}
```

### Step 8: Success Response

Server returns the analysis result:

```json
HTTP/1.1 200 OK

{
  "market": {
    "question": "Will Bitcoin reach $150,000 by Dec 31, 2025?",
    "yes_price": 0.08,
    "no_price": 0.92,
    "volume": 1250000
  },
  "analysis": {
    "consensus": "BUY_NO",
    "agreement": "5/6",
    "confidence": 82,
    "action": "Buy NO position"
  },
  "models": [
    {"name": "claude-opus", "action": "BUY_NO", "confidence": 85},
    {"name": "gpt-4o", "action": "BUY_NO", "confidence": 80},
    {"name": "gemini-pro", "action": "SKIP", "confidence": 60},
    {"name": "llama-405b", "action": "BUY_NO", "confidence": 75},
    {"name": "deepseek-v3", "action": "BUY_NO", "confidence": 82},
    {"name": "mistral-large", "action": "BUY_NO", "confidence": 78}
  ],
  "dissent": {
    "model": "gemini-pro",
    "action": "SKIP",
    "reason": "Macro uncertainty makes prediction difficult"
  },
  "meta": {
    "request_id": "req_a1b2c3d4e5f6",
    "cost": "$0.10",
    "network": "solana",
    "tx_signature": "5K7mNvuKR9vAqJNkqRV3f8WxYz..."
  }
}
```

---

## SDK Automatic Handling

Both SDKs handle this flow automatically:

### Python

```python
from nodo_x402 import NodoClient

# Client handles 402 → payment → retry automatically
client = NodoClient(keypair_path="~/.config/solana/id.json")

result = await client.analyze(
    market="polymarket.com/event/btc-150k",
    tier="deep"
)
# Payment of $0.10 sent and verified automatically!

print(result.consensus)  # "BUY_NO"
```

### TypeScript

```typescript
import { NodoClient } from '@nodo-ai/x402';

const client = new NodoClient({ keypair: keypair.secretKey });

const result = await client.analyze({
  market: 'polymarket.com/event/btc-150k',
  tier: 'deep'
});
// Payment of $0.10 sent and verified automatically!

console.log(result.analysis.consensus);  // "BUY_NO"
```

---

## Manual Payment Mode

For custom payment handling:

```python
from nodo_x402 import NodoClient, PaymentRequired

client = NodoClient(auto_pay=False)  # Disable auto-payment

try:
    result = await client.analyze(market="...")
except PaymentRequired as e:
    print(f"Payment needed: ${e.amount} USDC")
    print(f"Send to: {e.recipient}")
    print(f"Memo: {e.memo}")
    
    # Handle payment your own way
    tx_sig = await my_custom_payment(e.recipient, e.amount)
    
    # Then retry manually
    result = await client._request(
        "POST", "/analyze",
        json={"market": "..."},
        headers={"X-Payment-Tx": tx_sig}
    )
```

---

## Security

### For Clients
- Never expose private keys
- Verify recipient address matches expected NODO address
- Check amounts before signing

### For Server
- Always verify on-chain, never trust headers alone
- Track used transaction signatures (replay protection)
- Enforce transaction age limits
- Rate limit verification requests

---

## Error Scenarios

| Error | HTTP Code | Description |
|-------|-----------|-------------|
| No payment header | 402 | Return payment instructions |
| Invalid signature | 402 | Transaction not found |
| Wrong recipient | 402 | Payment sent to wrong address |
| Wrong amount | 402 | Payment amount doesn't match |
| Transaction too old | 402 | Payment expired (>5 min) |
| Already used | 402 | Replay attack detected |
| Transaction failed | 402 | On-chain transaction error |

