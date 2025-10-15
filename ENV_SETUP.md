# 🔐 Environment Variables Setup

## ✅ Security Update Complete

Your Sinch credentials have been moved to environment variables for security. The hardcoded credentials have been removed from `config.py`.

## 📝 Create .env File

Create a `.env` file in your project root with the following content:

```bash
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
```

## 🛡️ Security Features Added

### 1. .gitignore Protection
- ✅ `.env` file is now ignored by Git
- ✅ Won't be pushed to GitHub
- ✅ Protects your credentials

### 2. Environment Validation
- ✅ App validates required environment variables on startup
- ✅ Clear error messages if variables are missing
- ✅ Prevents app from running without proper configuration

### 3. Automatic .env Loading
- ✅ `python-dotenv` automatically loads `.env` file
- ✅ Works in both development and production

## 🚀 Quick Setup

### Option 1: Manual Creation
```bash
# Create .env file
touch .env

# Edit with your preferred editor
nano .env
# or
code .env
# or
vim .env
```

### Option 2: Copy from Template
```bash
# Copy the example file
cp env.example .env

# Edit with your actual credentials
nano .env
```

## 🧪 Test the Setup

After creating `.env`, test that everything works:

```bash
# Install updated dependencies
pip install -r requirements.txt

# Test the configuration
python3 -c "from config import *; print('✅ Configuration loaded successfully!')"

# Start the application
./start.sh
```

## 📋 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SINCH_ACCESS_KEY` | ✅ Yes | - | Your Sinch access key |
| `SINCH_ACCESS_SECRET` | ✅ Yes | - | Your Sinch access secret |
| `SINCH_PROJECT_ID` | ✅ Yes | - | Your Sinch project ID |
| `PHARMACY_FAX_NUMBER` | ❌ No | `17057415595` | Destination fax number |
| `PDF_SAVE_DIR` | ❌ No | `generated_pdfs` | Directory for PDF files |
| `CALLBACK_URL` | ❌ No | - | Optional callback URL |

## 🚨 Important Notes

### Development vs Production

**Development (Local):**
- Uses `.env` file
- Loaded automatically with `python-dotenv`

**Production (Render/Heroku):**
- Set environment variables in dashboard
- No `.env` file needed
- Variables are injected by the platform

### Render Deployment
When deploying to Render, set these environment variables in the Render dashboard:
- `SINCH_ACCESS_KEY`
- `SINCH_ACCESS_SECRET` 
- `SINCH_PROJECT_ID`
- `PHARMACY_FAX_NUMBER`
- `PDF_SAVE_DIR`
- `CALLBACK_URL` (optional)

## 🔧 Troubleshooting

### Error: "Missing required environment variables"
```bash
# Check if .env file exists
ls -la .env

# Verify .env file has correct format
cat .env

# Test loading
python3 -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('SINCH_ACCESS_KEY'))"
```

### Error: "ModuleNotFoundError: No module named 'dotenv'"
```bash
# Install python-dotenv
pip install python-dotenv

# Or reinstall all requirements
pip install -r requirements.txt
```

## 🎯 Next Steps

1. ✅ **Create `.env` file** with your credentials
2. ✅ **Test the setup** with the commands above
3. ✅ **Start the application** with `./start.sh`
4. ✅ **Deploy to Render** with environment variables set in dashboard

Your credentials are now secure and won't be pushed to GitHub! 🔒
