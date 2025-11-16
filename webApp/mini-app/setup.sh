#!/bin/bash

# Development Setup Script for Telegram Mini App

echo "🚀 Setting up Telegram Mini App Development Environment"
echo "=================================================="
echo ""

# Check if Node.js is installed
echo "📦 Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

NODE_VERSION=$(node -v)
echo "✅ Node.js $NODE_VERSION is installed"
echo ""

# Check if npm is installed
echo "📦 Checking npm installation..."
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

NPM_VERSION=$(npm -v)
echo "✅ npm $NPM_VERSION is installed"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo ""

# Check if API is running
echo "🔌 Checking if API is running..."
if curl -s http://localhost:8001/health > /dev/null; then
    echo "✅ API is running at http://localhost:8001"
else
    echo "⚠️  API is not running at http://localhost:8001"
    echo "   Please start your FastAPI backend first:"
    echo "   cd ~/app && source ~/virtualenv/app/3.11/bin/activate"
    echo "   python -m uvicorn api.main:app --host 0.0.0.0 --port 8001"
fi
echo ""

# Success message
echo "=================================================="
echo "✅ Setup complete!"
echo ""
echo "To start development:"
echo "  npm start"
echo ""
echo "To build for production:"
echo "  npm run build"
echo ""
echo "For testing in Telegram:"
echo "  1. Install ngrok: https://ngrok.com/download"
echo "  2. Run: ngrok http 4200"
echo "  3. Configure bot menu button with ngrok URL"
echo ""
echo "See QUICKSTART.md for detailed instructions"
echo "=================================================="

