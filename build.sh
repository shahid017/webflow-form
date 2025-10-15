#!/bin/bash

# Webflow Form to Fax API - Build Script

echo "🔨 Building Webflow Form to Fax API..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python version $python_version is too old. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p generated_pdfs
mkdir -p static

# Copy test form to static directory
if [ -f "test_form.html" ]; then
    echo "📋 Copying test form to static directory..."
    cp test_form.html static/
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your Sinch API credentials before running the application."
fi

# Run tests
echo "🧪 Running tests..."
python3 -c "
import sys
try:
    import fastapi
    import uvicorn
    import requests
    import fpdf
    print('✅ All dependencies installed successfully!')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    sys.exit(1)
"

echo ""
echo "🎉 Build completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your Sinch API credentials"
echo "2. Run: ./start.sh"
echo "3. Visit: http://localhost:8000/docs"
echo "4. Test with: http://localhost:8000/static/test_form.html"
echo ""
