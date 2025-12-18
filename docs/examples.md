# 📝 Examples

## Python Examples

### Basic Analysis

```python
import asyncio
from nodo_x402 import NodoClient

async def main():
    client = NodoClient(keypair_path="~/.config/solana/id.json")
    
    result = await client.analyze(
        market="polymarket.com/event/btc-150k-2025",
        tier="deep"
    )
    
    print(f"Consensus: {result.consensus}")
    print(f"Agreement: {result.agreement}")
    print(f"Confidence: {result.confidence}%")
    
    print("\nModel Votes:")
    for model in result.models:
        print(f"  {model.name}: {model.action} ({model.confidence}%)")
    
    if result.dissent:
        print(f"\nDissent: {result.dissent.model}")
        print(f"  Reason: {result.dissent.reason}")
    
    await client.close()

asyncio.run(main())
```

### Find Best Yield Opportunities

```python
async def find_best_yields():
    client = NodoClient(keypair_path="~/.config/solana/id.json")
    
    # Scan for opportunities
    opportunities = await client.yield_scan(
        min_probability=0.95,
        min_volume=10000,
        max_days=30,
        risk_level="LOW",
        limit=10
    )
    
    print(f"Found {len(opportunities)} opportunities\n")
    
    for i, opp in enumerate(opportunities, 1):
        print(f"{i}. {opp.question}")
        print(f"   Buy {opp.outcome} @ ${opp.buy_price:.3f}")
        print(f"   Profit: {opp.profit_pct:.2f}%")
        print(f"   APY: {opp.apy:.0f}%")
        print(f"   Risk: {opp.risk_level}")
        print()
    
    await client.close()
```

### Arbitrage Bot

```python
async def check_arbitrage():
    client = NodoClient(keypair_path="~/.config/solana/id.json")
    
    # Find arbitrage opportunities
    arbs = await client.arbitrage_scan(
        min_profit=1.0,  # 1% minimum
        min_volume=5000,
        limit=5
    )
    
    for arb in arbs:
        if arb["profit_pct"] > 2.0:
            print(f"🚨 HIGH PROFIT ARBITRAGE!")
            print(f"   Market: {arb['market_question']}")
            print(f"   Buy YES @ ${arb['yes_price']:.3f}")
            print(f"   Buy NO @ ${arb['no_price']:.3f}")
            print(f"   Total: ${arb['total_cost']:.3f}")
            print(f"   Guaranteed Profit: {arb['profit_pct']:.2f}%")
    
    await client.close()
```

### Trading Bot with AI

```python
class AITradingBot:
    def __init__(self, keypair_path: str):
        self.client = NodoClient(keypair_path=keypair_path)
        
    async def analyze_and_trade(self, market_url: str):
        # Get AI consensus
        analysis = await self.client.analyze(
            market=market_url,
            tier="deep"
        )
        
        # Only trade on high confidence consensus
        if analysis.confidence >= 80:
            agreement_parts = analysis.agreement.split("/")
            agreement_ratio = int(agreement_parts[0]) / int(agreement_parts[1])
            
            if agreement_ratio >= 0.8:  # 80% agreement
                print(f"Strong signal: {analysis.consensus}")
                print(f"Confidence: {analysis.confidence}%")
                print(f"Agreement: {analysis.agreement}")
                
                # Execute trade (implement your trading logic)
                # await self.execute_trade(market_url, analysis.consensus)
                
        await self.client.close()
```

### Monitor Multiple Markets

```python
async def monitor_markets():
    client = NodoClient(keypair_path="~/.config/solana/id.json")
    
    # Get all BTC-related markets
    markets = await client.get_markets(
        platform="polymarket",
        search="bitcoin",
        min_volume=50000,
        limit=20
    )
    
    print(f"Monitoring {len(markets)} BTC markets\n")
    
    for market in markets:
        # Quick analysis for each
        analysis = await client.analyze(
            market=market.url,
            tier="quick"  # $0.01 per market
        )
        
        print(f"{market.question[:50]}...")
        print(f"  Price: YES ${market.yes_price:.2f} / NO ${market.no_price:.2f}")
        print(f"  AI: {analysis.consensus} ({analysis.confidence}%)")
        print()
    
    await client.close()
```

---

## TypeScript Examples

### Basic Analysis

```typescript
import { NodoClient } from '@nodo-ai/x402';
import { Keypair } from '@solana/web3.js';
import fs from 'fs';

async function main() {
  const secretKey = JSON.parse(
    fs.readFileSync('~/.config/solana/id.json', 'utf8')
  );
  const keypair = Keypair.fromSecretKey(Uint8Array.from(secretKey));
  
  const client = new NodoClient({ keypair: keypair.secretKey });
  
  const result = await client.analyze({
    market: 'polymarket.com/event/btc-150k-2025',
    tier: 'deep',
  });
  
  console.log(`Consensus: ${result.analysis.consensus}`);
  console.log(`Agreement: ${result.analysis.agreement}`);
  console.log(`Confidence: ${result.analysis.confidence}%`);
  
  console.log('\nModel Votes:');
  for (const model of result.models) {
    console.log(`  ${model.name}: ${model.action} (${model.confidence}%)`);
  }
}

main();
```

### Yield Scanner

```typescript
async function findYields() {
  const client = new NodoClient({ keypair: keypair.secretKey });
  
  const opportunities = await client.yieldScan({
    minProbability: 0.95,
    minVolume: 10000,
    riskLevel: 'LOW',
    limit: 10,
  });
  
  console.log(`Found ${opportunities.length} opportunities\n`);
  
  for (const opp of opportunities) {
    console.log(`${opp.question}`);
    console.log(`  Buy ${opp.outcome} @ $${opp.buyPrice.toFixed(3)}`);
    console.log(`  APY: ${opp.apy.toFixed(0)}%`);
    console.log();
  }
}
```

### Webhook Handler (Express)

```typescript
import express from 'express';

const app = express();
app.use(express.json());

app.post('/nodo-webhook', (req, res) => {
  const { event, data, timestamp } = req.body;
  
  console.log(`Received ${event} at ${timestamp}`);
  
  switch (event) {
    case 'opportunity.yield':
      console.log(`New yield: ${data.question}`);
      console.log(`APY: ${data.apy}%`);
      // Handle yield opportunity
      break;
      
    case 'opportunity.delta':
      console.log(`Mispricing: ${data.logic_error}`);
      console.log(`Profit: ${data.profit_potential}%`);
      // Handle delta opportunity
      break;
      
    case 'market.resolved':
      console.log(`Market resolved: ${data.question}`);
      console.log(`Outcome: ${data.outcome}`);
      // Handle resolution
      break;
  }
  
  res.status(200).json({ received: true });
});

app.listen(3000);
```

---

## cURL Examples

### Get 402 Payment Details

```bash
curl -X POST https://api.nodo.ai/x402/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"market": "polymarket.com/event/btc-150k", "tier": "deep"}'
```

### Make Request with Payment

```bash
curl -X POST https://api.nodo.ai/x402/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-Payment-Tx: YOUR_SOLANA_TX_SIGNATURE" \
  -d '{"market": "polymarket.com/event/btc-150k", "tier": "deep"}'
```

### Yield Scan

```bash
curl "https://api.nodo.ai/x402/v1/yield/scan?min_probability=0.95&limit=10" \
  -H "X-Payment-Tx: YOUR_TX"
```

### Check Pricing

```bash
curl https://api.nodo.ai/x402/v1/account/pricing
```

