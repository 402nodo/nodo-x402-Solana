#!/bin/bash
# NODO x402 Protocol - Quick Start Script

set -e

echo "=========================================="
echo "  NODO x402 Protocol - Starting Server"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo "Creating from template..."
    cp env.example.txt .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env and add your API keys!"
    echo ""
    echo "Required variables:"
    echo "  - NODO_WALLET_ADDRESS"
    echo "  - OPENROUTER_API_KEY"
    echo "  - ANTHROPIC_API_KEY"
    echo "  - OPENAI_API_KEY"
    echo ""
    echo "Then run: ./start.sh"
    exit 1
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate venv
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "=========================================="
echo "  🚀 Starting FastAPI Server"
echo "=========================================="
echo ""
echo "Server will be available at:"
echo "  • http://localhost:8000"
echo "  • API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start server
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

