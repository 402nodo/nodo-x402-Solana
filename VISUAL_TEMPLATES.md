# 🎨 Visual Templates for Twitter Thread

Templates and suggestions for creating visuals for each tweet.

---

## 🛠️ Tools to Use

### Code Screenshots
- **Carbon.now.sh** - Beautiful code screenshots
- **Ray.so** - Modern code screenshots with gradients
- **CodeSnap** (VS Code extension) - Quick screenshots

### Diagrams
- **Excalidraw** - Hand-drawn style diagrams
- **Figma** - Professional diagrams
- **draw.io** - Free diagramming tool
- **Mermaid** - Code-to-diagram

### Graphics
- **Canva** - Quick graphics and charts
- **Figma** - Professional design
- **Photoshop** - Advanced editing

---

## 📸 Tweet 1: Main Code Example

### Content
```python
from nodo_x402 import NodoClient

client = NodoClient(keypair_path="~/.config/solana/id.json")
result = await client.analyze(
    market="polymarket.com/event/btc-150k-2025",
    tier="deep"  # 6 AI models
)

# Payment happens automatically! ✅
# - Detected 402 response
# - Sent 0.10 USDC on Solana (~400ms)
# - Got analysis from 6 AI models

print(f"Consensus: {result.consensus}")
print(f"Confidence: {result.confidence}%")

# Output:
# Consensus: BUY_NO
# Confidence: 87%
```

### Settings (Carbon/Ray)
- **Theme**: Monokai / One Dark
- **Language**: Python
- **Background**: Gradient (purple to blue)
- **Padding**: 64px
- **Drop shadow**: Yes
- **Font**: Fira Code / JetBrains Mono

### Alternative
Split screen:
- Left: Code
- Right: Output/result

---

## 📊 Tweet 2: Blockchain Comparison

### Content

Create a comparison table:

```
┌─────────────┬──────────┬──────────┬────────────┬────────────┐
│ Blockchain  │ Finality │ Fee      │ $0.01 Cost │ Viable?    │
├─────────────┼──────────┼──────────┼────────────┼────────────┤
│ Solana      │ 400ms    │ $0.00025 │ 2.5%       │ ✅ YES     │
│ Ethereum    │ 15 min   │ $5.00    │ 50,000%    │ ❌ NO      │
│ Polygon     │ 30s      │ $0.01    │ 100%       │ ❌ NO      │
│ Lightning   │ ~1min    │ $0.001   │ 10%        │ ⚠️ COMPLEX │
└─────────────┴──────────┴──────────┴────────────┴────────────┘

Example: 10,000 requests at $0.01 each

Solana:
  💰 Payment: $100.00
  💸 Fees:    $2.50
  📊 Total:   $102.50  ✅

Ethereum:
  💰 Payment: $100.00
  💸 Fees:    $15,000+
  📊 Total:   $15,100+ ❌
```

### Design Options

**Option 1: Bar Chart**
- Y-axis: Total cost
- X-axis: Blockchains
- Highlight Solana as lowest

**Option 2: Table**
- Clean table with checkmarks/X marks
- Use brand colors
- Add emoji for visual interest

**Option 3: Infographic**
- Split into 3 sections
- Show finality, fees, total cost
- Visual comparison

### Color Scheme
- Solana: Purple/Green (#14F195)
- Ethereum: Blue/Grey
- Polygon: Purple
- Background: Dark (#1a1a2e)

---

## 🔄 Tweet 3: Payment Flow Diagram

### Content

```
┌──────────┐
│  Client  │
│  (SDK)   │
└────┬─────┘
     │
     │ 1. POST /analyze
     ▼
┌──────────────┐
│    Server    │
│ x402 Check   │
└────┬─────────┘
     │
     │ 2. 402 Payment Required
     ▼         {amount: 0.10, recipient: ...}
┌──────────┐
│  Client  │
│  Pays    │
└────┬─────┘
     │
     │ 3. Send 0.10 USDC
     ▼         on Solana (400ms)
┌──────────────┐
│   Solana     │
│  Blockchain  │
└────┬─────────┘
     │
     │ 4. Retry with X-Payment-Tx: <signature>
     ▼
┌──────────────┐
│    Server    │
│  Verifies    │
└────┬─────────┘
     │
     │ 5. ✅ 200 OK
     ▼         {analysis: {...}}
┌──────────┐
│  Client  │
│  Success │
└──────────┘

Total time: ~500ms
```

### Design Options

**Option 1: Linear Flow**
- Vertical arrows
- 5 steps clearly numbered
- Icons for each component

**Option 2: Circular Flow**
- Show it as a loop
- Emphasize speed (500ms)

**Option 3: Before/After**
- Left: Manual (complex)
- Right: SDK (automatic)

### Elements
- Icons: 💻 (client), 🌐 (server), ⚡ (Solana)
- Colors: Use Solana purple/green
- Timestamps: Show 400ms, 500ms
- Checkmarks: ✅ for success steps

---

## 🤖 Tweet 4: Multi-AI Parallel Execution

### Content

```
Market Data
     │
     ▼
┌────────────────────────────────────────┐
│        AI Orchestrator                 │
│     (Parallel Execution)               │
└┬───┬───┬───┬────┬────┬────────────────┘
 │   │   │   │    │    │
 ▼   ▼   ▼   ▼    ▼    ▼
┌─┐ ┌─┐ ┌─┐ ┌──┐ ┌──┐ ┌───┐
│C│ │G│ │G│ │L │ │D │ │M  │
│l│ │P│ │e│ │l │ │e │ │i  │
│a│ │T│ │m│ │a │ │e │ │s  │
│u│ │-│ │i│ │m │ │p │ │t  │
│d│ │4│ │n│ │a │ │S │ │r  │
│e│ │o│ │i│ │4 │ │e │ │a  │
│ │ │ │ │ │ │0 │ │e │ │l  │
│ │ │ │ │ │ │5 │ │k │ │   │
│ │ │ │ │ │ │B │ │  │ │   │
└─┘ └─┘ └─┘ └──┘ └──┘ └───┘
 │   │   │   │    │    │
 └───┴───┴───┴────┴────┘
           │
           ▼
    ┌──────────────┐
    │  Consensus   │
    │  Algorithm   │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Recommendation│
    │ Confidence: 87%│
    └──────────────┘

Time: 2-3 seconds (all parallel)
vs 12+ seconds (sequential)
```

### Design Options

**Option 1: Hexagon Grid**
- 6 hexagons for 6 AI models
- Center hexagon = consensus
- Modern, tech-y look

**Option 2: Timeline**
- Show all models start at t=0
- All finish at t=2-3s
- Consensus aggregated

**Option 3: Circuit Board**
- Tech aesthetic
- Lines connecting models to consensus
- Neon colors

### Elements
- AI Model Logos (if available)
- Model names clearly visible
- Arrows showing data flow
- Time indicators (2-3s)
- Highlight parallel execution

---

## 🏗️ Tweet 5: System Architecture

### Content

```
┌─────────────────────────────────────────────┐
│                                             │
│  ┌──────────┐                               │
│  │  Client  │  ← Users/AI Agents            │
│  │  (SDK)   │                               │
│  └────┬─────┘                               │
│       │                                      │
│       │ HTTP + x402                          │
│       ▼                                      │
│  ┌──────────────────────────┐               │
│  │    FastAPI Server        │               │
│  │  ┌────────────────────┐  │               │
│  │  │ x402 Middleware    │  │ ← Intercept   │
│  │  └────────┬───────────┘  │               │
│  │           │               │               │
│  │  ┌────────▼───────────┐  │               │
│  │  │ Payment Verifier   │  │ ← Check tx    │
│  │  └────────┬───────────┘  │               │
│  │           │               │               │
│  │  ┌────────▼───────────┐  │               │
│  │  │   API Endpoints    │  │ ← Business    │
│  │  │  • /analyze        │  │   logic       │
│  │  │  • /yield/scan     │  │               │
│  │  │  • /delta/scan     │  │               │
│  │  └────────────────────┘  │               │
│  └──────────────────────────┘               │
│              │                               │
│              │ Solana RPC                    │
│              ▼                               │
│  ┌──────────────────────────┐               │
│  │   Solana Blockchain      │               │
│  │   • Verify transactions  │               │
│  │   • Check USDC transfers │               │
│  │   • 400ms finality       │               │
│  └──────────────────────────┘               │
│                                             │
└─────────────────────────────────────────────┘
```

### Design Options

**Option 1: Layered Stack**
- Show as layers
- Client → Server → Middleware → Solana
- Clean, minimal

**Option 2: Flow Diagram**
- Detailed with arrows
- Show request/response flow
- Include status codes (402, 200)

**Option 3: Component Diagram**
- Boxes for each component
- Clear separation of concerns
- Professional look

### Elements
- Use Solana brand colors
- Clear labels for each layer
- Show data flow with arrows
- Highlight x402 middleware layer
- Include timing (~450ms)

---

## 💻 Tweet 6: SDK Code Example

### Content

```typescript
import { NodoClient } from '@nodo-ai/x402';

class TradingBot {
  private client: NodoClient;
  
  constructor(keypair: Uint8Array) {
    this.client = new NodoClient({ keypair });
  }
  
  async analyzeMarket(market: string) {
    // Bot pays automatically from its wallet
    const analysis = await this.client.analyze({
      market: market,
      tier: 'standard'  // $0.05
    });
    
    if (analysis.confidence > 80) {
      console.log(`🎯 High confidence: ${analysis.consensus}`);
      await this.executeTrade(analysis.consensus);
    } else {
      console.log(`⚠️ Low confidence: ${analysis.confidence}%`);
    }
  }
  
  async run() {
    const markets = await this.getMarkets();
    
    // Analyze 100 markets in parallel
    console.log(`🔍 Analyzing ${markets.length} markets...`);
    
    await Promise.all(
      markets.map(m => this.analyzeMarket(m))
    );
    
    console.log('✅ Complete! Total: $5, Time: ~3s');
  }
}

// Usage:
const bot = new TradingBot(loadKeypair());
await bot.run();
```

### Settings
- **Theme**: GitHub Dark / Tokyo Night
- **Language**: TypeScript
- **Highlight**: Async/await, auto-payment
- **Annotations**: Add arrows/notes pointing to key features

### Alternative
Split screen:
- Left: TypeScript code
- Right: Console output showing execution

---

## 📦 Tweet 7: GitHub Repository Preview

### Content

Create a visual showing:

```
┌─────────────────────────────────────────┐
│  📦 nodo-x402-protocol                  │
│  ⭐ 47 stars  🍴 12 forks              │
├─────────────────────────────────────────┤
│                                         │
│  AI Market Analysis with x402 on Solana │
│                                         │
│  📁 Structure:                          │
│  ├── src/            ✅ FastAPI server │
│  ├── sdk/            ✅ Python & TS    │
│  ├── docs/           ✅ 17 pages       │
│  └── examples/       ✅ 3 demos        │
│                                         │
│  📊 Stats:                              │
│  • 75 files                             │
│  • 15,000+ lines                        │
│  • Production-ready                     │
│  • MIT License                          │
│                                         │
│  🚀 Quick Start:                        │
│  $ git clone repo                       │
│  $ docker-compose up                    │
│                                         │
└─────────────────────────────────────────┘
```

### Design Options

**Option 1: GitHub Screenshot**
- Real screenshot of repo
- Show README preview
- Include star count

**Option 2: Infographic**
- File structure visualization
- Stats prominently displayed
- Call to action (Star repo)

**Option 3: Collage**
- Multiple screenshots
- Code snippets
- Documentation preview
- Directory tree

### Elements
- GitHub star button (visual)
- File structure
- Key stats (75 files, etc)
- MIT License badge
- Quick start commands

---

## 🎨 General Design Guidelines

### Color Palette
```
Primary:   #14F195 (Solana Green)
Secondary: #9945FF (Solana Purple)
Dark:      #1a1a2e
Light:     #eeffee
Accent:    #00d9ff
```

### Typography
- **Headings**: SF Pro Display / Inter Bold
- **Code**: Fira Code / JetBrains Mono
- **Body**: Inter / SF Pro Text

### Layout
- **Padding**: Generous (64px+)
- **Shadows**: Subtle drop shadows
- **Gradients**: Purple to blue/green
- **Icons**: Consistent style (phosphor, lucide)

### Accessibility
- High contrast text
- Large readable fonts
- Clear visual hierarchy
- Don't rely only on color

---

## 📐 Image Dimensions

### Twitter Optimal Sizes
- **Single image**: 1200x675px (16:9)
- **Code screenshot**: 1600x900px (high DPI)
- **Diagram**: 1200x1200px (square works well)

### Export Settings
- **Format**: PNG (for transparency)
- **Quality**: High (80-90%)
- **Compression**: Optimize for web

---

## 🛠️ Quick Creation Workflow

### For Code Screenshots (2 min)

1. Open Carbon.now.sh or Ray.so
2. Paste code
3. Select theme (One Dark / Monokai)
4. Adjust padding (64px)
5. Add background gradient
6. Export PNG

### For Diagrams (10 min)

1. Open Excalidraw or Figma
2. Use template above
3. Add icons/shapes
4. Apply color scheme
5. Export PNG

### For Tables/Charts (5 min)

1. Create in Canva or Figma
2. Use brand colors
3. Make text large and readable
4. Export PNG

---

## ✅ Final Checklist

Before posting each image:

- [ ] Text is readable on mobile
- [ ] Colors are on-brand
- [ ] Image is high quality
- [ ] File size < 5MB
- [ ] Dimensions optimal for Twitter
- [ ] No sensitive information visible
- [ ] Compressed for web

---

## 💡 Pro Tips

1. **Consistency**: Use same style across all images
2. **Branding**: Include subtle branding (logo/color)
3. **Mobile**: Test how it looks on small screens
4. **Contrast**: Ensure good readability
5. **Simplicity**: Less is more, avoid clutter
6. **Preview**: Check how Twitter crops it

---

Ready to create amazing visuals! 🎨

