#!/usr/bin/env python3
"""
Manual Payment Example
Shows how to handle x402 payments manually without auto-pay.
"""
import asyncio
from nodo_x402 import NodoClient, PaymentRequired
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from spl.token.instructions import transfer_checked, get_associated_token_address


async def send_usdc_manually(
    keypair: Keypair,
    recipient: str,
    amount: float,
    memo: str
):
    """Send USDC payment manually."""
    print(f"Sending ${amount} USDC to {recipient[:8]}...")
    print(f"Memo: {memo}")
    
    client = AsyncClient("https://api.mainnet-beta.solana.com")
    
    # USDC mint
    usdc_mint = Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
    recipient_pubkey = Pubkey.from_string(recipient)
    
    # Get token accounts
    sender_token = get_associated_token_address(keypair.pubkey(), usdc_mint)
    recipient_token = get_associated_token_address(recipient_pubkey, usdc_mint)
    
    # Build transaction
    tx = Transaction()
    
    # Add memo
    if memo:
        from spl.memo.instructions import create_memo, MemoParams
        tx.add(create_memo(MemoParams(
            signer=keypair.pubkey(),
            message=memo.encode()
        )))
    
    # Add USDC transfer
    amount_lamports = int(amount * 1_000_000)  # USDC has 6 decimals
    tx.add(transfer_checked(
        source=sender_token,
        mint=usdc_mint,
        dest=recipient_token,
        owner=keypair.pubkey(),
        amount=amount_lamports,
        decimals=6
    ))
    
    # Send transaction
    response = await client.send_transaction(tx, keypair)
    signature = str(response.value)
    
    print(f"✅ Transaction sent: {signature[:16]}...")
    print(f"⏱️ Waiting for confirmation...")
    
    # Wait for confirmation
    await client.confirm_transaction(response.value)
    
    print(f"✅ Transaction confirmed!")
    await client.close()
    
    return signature


async def main():
    print("=" * 60)
    print("  x402 Manual Payment Example")
    print("=" * 60)
    print()
    
    # Load keypair
    import json
    with open("~/.config/solana/id.json") as f:
        keypair = Keypair.from_bytes(bytes(json.load(f)))
    
    # Initialize client WITHOUT auto-pay
    client = NodoClient(
        keypair_path="~/.config/solana/id.json",
        auto_pay=False  # ← Manual mode
    )
    
    try:
        print("1. Making request without payment...")
        result = await client.analyze(
            market="polymarket.com/event/btc-150k-2025",
            tier="quick"
        )
        
    except PaymentRequired as e:
        print("2. ❌ Got 402 Payment Required")
        print(f"   Amount: ${e.amount}")
        print(f"   Recipient: {e.recipient[:8]}...")
        print(f"   Memo: {e.memo}")
        print()
        
        print("3. Sending payment manually...")
        tx_signature = await send_usdc_manually(
            keypair=keypair,
            recipient=e.recipient,
            amount=e.amount,
            memo=e.memo
        )
        print()
        
        print("4. Retrying request with payment proof...")
        result = await client.analyze(
            market="polymarket.com/event/btc-150k-2025",
            tier="quick",
            headers={"X-Payment-Tx": tx_signature}  # ← Proof
        )
        
        print("5. ✅ Success!")
        print(f"   Consensus: {result.consensus}")
        print(f"   Confidence: {result.confidence}%")
    
    await client.close()
    
    print()
    print("=" * 60)
    print("  Manual payment flow completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

