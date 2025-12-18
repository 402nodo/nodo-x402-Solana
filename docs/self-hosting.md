# 🖥️ Self-Hosting

## Overview

Run your own NODO x402 server for development, testing, or custom deployments.

---

## Requirements

- Python 3.11+
- PostgreSQL (optional, for production)
- Redis (optional, for caching)
- Solana RPC access
- AI API keys (OpenRouter, Anthropic, OpenAI)

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/nodo-ai/nodo-x402-protocol.git
cd nodo-x402-protocol
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp env.example.txt .env
```

Edit `.env` with your settings:

```bash
# Solana
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
NODO_WALLET_ADDRESS=YOUR_SOLANA_WALLET_ADDRESS
NODO_PRIVATE_KEY=YOUR_PRIVATE_KEY

# AI APIs (at least one required)
OPENROUTER_API_KEY=your_openrouter_key
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key

# Server
DEBUG=true
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

### 5. Run Server

```bash
# Development
python -m uvicorn src.main:app --reload

# Production
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Server available at: http://localhost:8000

- Swagger UI: http://localhost:8000/docs
- x402 Info: http://localhost:8000/x402/info

---

## Configuration

### Environment Variables

#### Solana Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SOLANA_RPC_URL` | No | mainnet | Solana RPC endpoint |
| `SOLANA_WS_URL` | No | mainnet | WebSocket endpoint |
| `SOLANA_USDC_MINT` | No | mainnet USDC | USDC token mint |
| `NODO_WALLET_ADDRESS` | **Yes** | - | Payment receiving wallet |
| `NODO_PRIVATE_KEY` | No | - | For signing (optional) |
| `PAYMENT_CONFIRMATION_TIMEOUT` | No | 30 | Seconds to wait |

#### AI API Keys

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Recommended | Access to multiple models |
| `ANTHROPIC_API_KEY` | Optional | Direct Claude access |
| `OPENAI_API_KEY` | Optional | Direct GPT-4 access |
| `GOOGLE_API_KEY` | Optional | Direct Gemini access |

At least one AI API key is required. OpenRouter provides access to all models.

#### Server Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | false | Enable debug mode |
| `LOG_LEVEL` | INFO | Logging level |
| `HOST` | 0.0.0.0 | Bind host |
| `PORT` | 8000 | Bind port |
| `CORS_ORIGINS` | * | Allowed origins |
| `RATE_LIMIT_PER_MINUTE` | 60 | Rate limit |

#### Pricing Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PRICE_AI_QUICK` | 0.01 | Quick tier price |
| `PRICE_AI_STANDARD` | 0.05 | Standard tier |
| `PRICE_AI_DEEP` | 0.10 | Deep tier |
| `PRICE_YIELD_SCAN` | 0.005 | Yield scanner |
| `PRICE_DELTA_SCAN` | 0.01 | Delta scanner |
| `PRICE_SMART_ANALYZE` | 0.02 | Smart analyzer |
| `PRICE_ARBITRAGE_SCAN` | 0.01 | Arbitrage scanner |
| `PRICE_MARKET_DATA` | 0.001 | Market data |

---

## Development Mode

For local development without real payments:

```bash
# .env
DEBUG=true
SOLANA_RPC_URL=https://api.devnet.solana.com
```

In debug mode, the Solana client uses mock verification that accepts any valid-looking transaction signature.

---

## Production Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```bash
docker build -t nodo-x402 .
docker run -p 8000:8000 --env-file .env nodo-x402
```

### Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

### Railway

1. Connect GitHub repository
2. Add environment variables
3. Deploy

### Fly.io

```bash
fly launch
fly secrets set OPENROUTER_API_KEY=xxx NODO_WALLET_ADDRESS=xxx
fly deploy
```

---

## Database (Optional)

For tracking usage and payments:

```bash
# .env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/nodo_x402
```

Run migrations:

```bash
alembic upgrade head
```

---

## Redis Cache (Optional)

For improved performance:

```bash
# .env
REDIS_URL=redis://localhost:6379/0
```

---

## SSL/HTTPS

For production, use a reverse proxy:

### Nginx

```nginx
server {
    listen 443 ssl;
    server_name api.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Caddy

```
api.yourdomain.com {
    reverse_proxy localhost:8000
}
```

---

## Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

### Logs

```bash
# View logs
docker logs -f nodo-x402

# Log level
LOG_LEVEL=DEBUG python -m uvicorn src.main:app
```

### Metrics

The server exposes metrics at `/metrics` (if enabled):

- Request count
- Response times
- Payment verification times
- AI model latencies

---

## Security Checklist

- [ ] Use HTTPS in production
- [ ] Secure private keys (use secrets manager)
- [ ] Set proper CORS origins
- [ ] Enable rate limiting
- [ ] Use read-only RPC when possible
- [ ] Monitor for unusual activity
- [ ] Keep dependencies updated

