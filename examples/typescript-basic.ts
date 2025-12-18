/**
 * Basic x402 Example (TypeScript)
 * Demonstrates simple API request with automatic payment.
 */
import { NodoClient } from '@nodo-ai/x402';
import { Keypair } from '@solana/web3.js';
import fs from 'fs';

async function main() {
  console.log('='.repeat(60));
  console.log('  x402 Protocol - Basic Example');
  console.log('='.repeat(60));
  console.log();

  // Load Solana keypair
  const keypairFile = fs.readFileSync(
    process.env.HOME + '/.config/solana/id.json'
  );
  const keypair = Keypair.fromSecretKey(
    Uint8Array.from(JSON.parse(keypairFile.toString()))
  );

  // Initialize client
  const client = new NodoClient({
    keypair: keypair.secretKey,
  });

  console.log('Making API request...');
  console.log('→ POST /analyze');
  console.log('  market: polymarket.com/event/btc-150k-2025');
  console.log('  tier: quick ($0.01)');
  console.log();

  // Make request - payment happens automatically
  const result = await client.analyze({
    market: 'polymarket.com/event/btc-150k-2025',
    tier: 'quick', // $0.01
  });

  console.log('✅ Request successful!');
  console.log();
  console.log(`Consensus: ${result.analysis.consensus}`);
  console.log(`Confidence: ${result.analysis.confidence}%`);
  console.log(`Agreement: ${result.analysis.agreement}`);
  console.log();
  console.log(`💰 Payment: ${result.meta.cost}`);
  console.log(`📝 Request ID: ${result.meta.requestId}`);
  console.log();

  console.log('='.repeat(60));
  console.log('  Payment flow completed automatically!');
  console.log('  • Detected 402 response');
  console.log('  • Sent 0.01 USDC on Solana');
  console.log('  • Retried with payment proof');
  console.log('  • Got analysis result');
  console.log('='.repeat(60));
}

main().catch(console.error);

