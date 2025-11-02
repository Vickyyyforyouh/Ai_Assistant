#!/bin/bash
# AI Agent Startup Script for macOS

echo "🤖 Starting AI Agent Backend..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3 from https://www.python.org/downloads/macos/"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/bin/flask" ]; then
    echo "📥 Installing dependencies..."
    pip3 install -r requirements.txt
    echo "✓ Dependencies installed"
    echo ""
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create .env with your API key"
    echo ""
fi

# Start the server
echo "🚀 Starting Flask server..."
echo "Server will run at: http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""
python3 app.py
