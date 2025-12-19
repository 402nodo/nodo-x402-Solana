# 🚀 Quick Start Guide

Get your x402 server running in 5 minutes.

## Prerequisites

- Python 3.11+
- Solana wallet with USDC
- API keys (OpenRouter, Anthropic, OpenAI)

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/nodo-x402-protocol
cd nodo-x402-protocol
```

## 2. Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using Make
make install
```

## 3. Configure Environment

```bash
# Copy example config
cp env.example.txt .env

# Edit .env with your keys
nano .env
```

Required variables:
```bash
# Solana
NODO_WALLET_ADDRESS=YourSolanaAddressHere
NODO_PRIVATE_KEY=YourPrivateKeyHere

# AI APIs
OPENROUTER_API_KEY=sk-or-...
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Pricing (optional, defaults work)
PRICE_AI_DEEP=0.10
```

## 4. Run Server

### Option A: Direct

```bash
python -m uvicorn src.main:app --reload
```

### Option B: Make

```bash
make run
```

### Option C: Docker

```bash
docker-compose up
```

Server will start at: **http://localhost:8000**

## 5. Test It Works

### Check Health

```bash
curl http://localhost:8000/health
```

### View API Docs

Open in browser: **http://localhost:8000/docs**

### Test x402 Payment

```bash
# Request without payment - get 402
curl http://localhost:8000/analyze \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"market": "polymarket.com/event/btc-150k", "tier": "quick"}'

# Response: 402 Payment Required
```

## 6. Use SDK

### Python

```bash
pip install nodo-x402
```

```python
from nodo_x402 import NodoClient

client = NodoClient(keypair_path="~/.config/solana/id.json")
result = await client.analyze(market="...", tier="quick")
print(result.consensus)
```

### TypeScript

```bash
npm install @nodo-ai/x402
```

```typescript
import { NodoClient } from '@nodo-ai/x402';

const client = new NodoClient({ keypair: keypair.secretKey });
const result = await client.analyze({ market: '...', tier: 'quick' });
```

## Testing

### Run Tests

```bash
pytest
# or
make test
```

### Use Devnet

For testing, use Solana devnet:

```bash
# In .env
SOLANA_RPC_URL=https://api.devnet.solana.com
```

Get devnet tokens:
```bash
solana airdrop 1 --url devnet
```

## Production Deployment

### Railway

```bash
railway up
```

### Fly.io

```bash
fly deploy
```

### Docker

```bash
docker build -t nodo-x402 .
docker run -p 8000:8000 --env-file .env nodo-x402
```

## Common Issues

### "No API key" errors

Make sure `.env` file exists and contains valid API keys.

### "Solana RPC error"

Check your `SOLANA_RPC_URL` is correct and accessible.

### "Payment verification failed"

- Check wallet address is correct
- Ensure transaction was confirmed
- Verify USDC transfer amount matches

## Next Steps

- Read [Full Documentation](README.md)
- Check [API Reference](docs/api.md)
- See [Examples](examples/)
- Join [Discord](https://discord.gg/nodo)

## Support

- 📧 dev@nodo.ai
- 💬 Discord: https://discord.gg/nodo
- 🐛 Issues: https://github.com/YOUR_USERNAME/nodo-x402-protocol/issues

