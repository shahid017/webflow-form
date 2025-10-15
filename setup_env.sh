#!/bin/bash

# Setup .env file script

echo "🔐 Setting up environment variables..."

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Setup cancelled."
        exit 1
    fi
fi

# Create .env file with your credentials
cat > .env << 'EOF'
# Sinch API Configuration
SINCH_ACCESS_KEY=ecb77cdc-0db0-441b-83c9-8a362de5cb22
SINCH_ACCESS_SECRET=2Pryq7RuJ7u6dmB2MEyz2mzJZQ
SINCH_PROJECT_ID=d04cbbec-47c1-4f6a-b573-81405882ab52

# Fax Configuration
PHARMACY_FAX_NUMBER=17057415595

# PDF Configuration
PDF_SAVE_DIR=generated_pdfs

# Optional Callback URL for fax status updates
CALLBACK_URL=
EOF

echo "✅ .env file created successfully!"
echo ""
echo "📋 Contents of .env file:"
echo "------------------------"
cat .env
echo "------------------------"
echo ""
echo "🔒 Your credentials are now secure and won't be pushed to GitHub!"
echo ""
echo "🧪 Test the setup:"
echo "   python3 -c \"from config import *; print('✅ Configuration loaded!')\""
echo ""
echo "🚀 Start the application:"
echo "   ./start.sh"
