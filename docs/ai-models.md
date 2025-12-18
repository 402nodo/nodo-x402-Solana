# 🤖 AI Models

## Overview

NODO x402 uses 6 AI models for consensus analysis. Each model brings unique strengths to the analysis.

---

## Model Roster

### 1. Claude Opus (Anthropic)

| Attribute | Value |
|-----------|-------|
| **Provider** | Anthropic |
| **Model ID** | claude-3-opus-20240229 |
| **Tier** | Quick, Standard, Deep |
| **Strength** | Complex reasoning |

**Best for:**
- Nuanced market analysis
- Understanding complex event conditions
- Identifying edge cases

**API**: Direct Anthropic API (fallback: OpenRouter)

---

### 2. GPT-4o (OpenAI)

| Attribute | Value |
|-----------|-------|
| **Provider** | OpenAI |
| **Model ID** | gpt-4o |
| **Tier** | Standard, Deep |
| **Strength** | General analysis |

**Best for:**
- Broad market understanding
- Historical pattern recognition
- Clear explanations

**API**: Direct OpenAI API (fallback: OpenRouter)

---

### 3. Gemini Pro (Google)

| Attribute | Value |
|-----------|-------|
| **Provider** | Google |
| **Model ID** | gemini-1.5-pro |
| **Tier** | Standard, Deep |
| **Strength** | Data synthesis |

**Best for:**
- Processing large data contexts
- Combining multiple data sources
- Quantitative analysis

**API**: Direct Google AI API (fallback: OpenRouter)

---

### 4. Llama 405B (Meta)

| Attribute | Value |
|-----------|-------|
| **Provider** | Meta (via OpenRouter) |
| **Model ID** | meta-llama/llama-3.1-405b-instruct |
| **Tier** | Deep only |
| **Strength** | Alternative perspective |

**Best for:**
- Independent viewpoint
- Challenging consensus
- Open-source transparency

**API**: OpenRouter

---

### 5. DeepSeek V3 (DeepSeek)

| Attribute | Value |
|-----------|-------|
| **Provider** | DeepSeek (via OpenRouter) |
| **Model ID** | deepseek/deepseek-chat |
| **Tier** | Deep only |
| **Strength** | Financial analysis |

**Best for:**
- Quantitative reasoning
- Financial market analysis
- Risk assessment

**API**: OpenRouter

---

### 6. Mistral Large (Mistral)

| Attribute | Value |
|-----------|-------|
| **Provider** | Mistral (via OpenRouter) |
| **Model ID** | mistralai/mistral-large-latest |
| **Tier** | Deep only |
| **Strength** | European perspective |

**Best for:**
- Multilingual analysis
- European market context
- Regulatory considerations

**API**: OpenRouter

---

## Tier Model Selection

```
┌─────────────────────────────────────────────────────────┐
│                    TIER SELECTION                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  QUICK ($0.01)                                          │
│  └── Claude Opus                                        │
│                                                          │
│  STANDARD ($0.05)                                       │
│  ├── Claude Opus                                        │
│  ├── GPT-4o                                             │
│  └── Gemini Pro                                         │
│                                                          │
│  DEEP ($0.10)                                           │
│  ├── Claude Opus                                        │
│  ├── GPT-4o                                             │
│  ├── Gemini Pro                                         │
│  ├── Llama 405B                                         │
│  ├── DeepSeek V3                                        │
│  └── Mistral Large                                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Consensus Algorithm

### 1. Parallel Execution

All selected models receive the same prompt simultaneously:

```python
tasks = [analyze_with_model(m, market) for m in models]
results = await asyncio.gather(*tasks)
```

### 2. Response Parsing

Each model returns:
- **Action**: `BUY_YES`, `BUY_NO`, or `SKIP`
- **Confidence**: 1-100
- **Reasoning**: Brief explanation

### 3. Weighted Voting

Votes are weighted by confidence:

```python
votes = {"BUY_YES": 0, "BUY_NO": 0, "SKIP": 0}

for result in results:
    votes[result.action] += result.confidence

consensus = max(votes, key=votes.get)
```

### 4. Agreement Calculation

```python
agreement_count = sum(1 for r in results if r.action == consensus)
agreement = f"{agreement_count}/{len(results)}"  # e.g., "5/6"
```

### 5. Dissent Identification

If any model disagrees with consensus, the highest-confidence dissenter is highlighted:

```python
dissenters = [r for r in results if r.action != consensus]
if dissenters:
    dissent = max(dissenters, key=lambda x: x.confidence)
```

---

## Analysis Prompt

Each model receives this structured prompt:

```
Analyze this prediction market:

MARKET: {question}
YES Price: ${yes_price} ({probability}% implied probability)
NO Price: ${no_price} ({100-probability}% implied probability)
Volume: ${volume}
End Date: {end_date}

Strategy: {strategy_context}

Provide a brief analysis (max 150 words) in this format:
ACTION: [BUY_YES / BUY_NO / SKIP]
CONFIDENCE: [1-100]
REASONING: [2-3 sentences explaining your decision]

Be concise and decisive.
```

---

## Fallback Chain

If a model's direct API fails, the system falls back to OpenRouter:

```
Claude → Anthropic API → OpenRouter (anthropic/claude-3-opus)
GPT-4  → OpenAI API    → OpenRouter (openai/gpt-4o)
Gemini → Google API    → OpenRouter (google/gemini-1.5-pro)
```

This ensures high availability even if individual APIs are down.

---

## Model Performance

Typical response times:

| Model | Avg Response | P95 Response |
|-------|--------------|--------------|
| Claude Opus | 2.5s | 5s |
| GPT-4o | 2.0s | 4s |
| Gemini Pro | 1.8s | 3.5s |
| Llama 405B | 3.0s | 6s |
| DeepSeek V3 | 2.2s | 4.5s |
| Mistral Large | 2.0s | 4s |

**Total Analysis Time:**
- Quick: ~2-3s (1 model)
- Standard: ~3-5s (3 models parallel)
- Deep: ~5-10s (6 models parallel)

---

## Adding Custom Models

To add a new model, update `AI_MODELS` in `ai_orchestrator.py`:

```python
AI_MODELS = [
    # ... existing models ...
    AIModelConfig(
        name="your-model",
        provider="openrouter",
        model_id="provider/model-name",
        api_key_setting="openrouter_api_key",
        description="What this model is good at"
    ),
]
```

