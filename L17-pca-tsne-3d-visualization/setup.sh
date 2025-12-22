#!/bin/bash
# Quick setup script for Assignment 17 (Mac/Linux)

echo "🚀 Setting up Assignment 17..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✨ Setup complete!"
echo ""
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the code:"
echo "  python main.py"