#!/bin/bash

# Webflow Form to Fax API - Start Script

echo "🚀 Starting Webflow Form to Fax API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create generated_pdfs directory if it doesn't exist
if [ ! -d "generated_pdfs" ]; then
    echo "📁 Creating generated_pdfs directory..."
    mkdir generated_pdfs
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Please copy env.example to .env and configure your settings:"
    echo "   cp env.example .env"
    echo "   Then edit .env with your Sinch API credentials"
    echo ""
    echo "🔧 Using default configuration for now..."
fi

# Start the server
echo "🌐 Starting FastAPI server..."
echo "📋 API Documentation: http://localhost:8000/docs"
echo "🧪 Test Form: http://localhost:8000/static/test_form.html"
echo ""

# Use PORT environment variable if available (for Render), otherwise use 8000
PORT=${PORT:-8000}
uvicorn main:app --host 0.0.0.0 --port $PORT --reload
