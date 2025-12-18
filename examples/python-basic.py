#!/usr/bin/env python3
"""
Basic x402 Example (Python)
Demonstrates simple API request with automatic payment.
"""
import asyncio
from nodo_x402 import NodoClient


async def main():
    print("=" * 60)
    print("  x402 Protocol - Basic Example")
    print("=" * 60)
    print()
    
    # Initialize client with Solana keypair
    client = NodoClient(
        keypair_path="~/.config/solana/id.json"
    )
    
    print("Making API request...")
    print("→ POST /analyze")
    print("  market: polymarket.com/event/btc-150k-2025")
    print("  tier: quick ($0.01)")
    print()
    
    # Make request - payment happens automatically
    result = await client.analyze(
        market="polymarket.com/event/btc-150k-2025",
        tier="quick"  # $0.01
    )
    
    print("✅ Request successful!")
    print()
    print(f"Consensus: {result.consensus}")
    print(f"Confidence: {result.confidence}%")
    print(f"Agreement: {result.agreement}")
    print()
    print(f"💰 Payment: {result.cost}")
    print(f"📝 Request ID: {result.request_id}")
    print()
    
    await client.close()
    
    print("=" * 60)
    print("  Payment flow completed automatically!")
    print("  • Detected 402 response")
    print("  • Sent 0.01 USDC on Solana")
    print("  • Retried with payment proof")
    print("  • Got analysis result")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

