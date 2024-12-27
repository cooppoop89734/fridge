#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting build process..."

# Check Python version
echo "📝 Checking Python version..."
python3 --version

# Create and activate virtual environment
echo "🔧 Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "📦 Installing development dependencies..."
pip install pylint pytest mypy types-Pillow

# Run syntax check
echo "🔍 Running syntax check..."
python3 -m py_compile app.py

# Run type checking
echo "🔍 Running type check..."
mypy app.py --ignore-missing-imports || true

# Run pylint
echo "🔍 Running code analysis..."
pylint app.py || true

# Run tests (if they exist)
if [ -d "tests" ]; then
    echo "🧪 Running tests..."
    pytest tests/
fi

echo "✅ Build process completed successfully!" 