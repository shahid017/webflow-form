# 🚀 Build & Start Commands

## Quick Start

### 1. Build the Application
```bash
./build.sh
```

### 2. Configure Environment
```bash
# Copy environment template
cp env.example .env

# Edit .env with your Sinch API credentials
nano .env  # or use your preferred editor
```

### 3. Start the Application
```bash
./start.sh
```

## Alternative Commands

### Build Only
```bash
./build.sh
```

### Start Only (if already built)
```bash
./start.sh
```

### Development Mode (with auto-reload)
```bash
./start.sh
# or
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Test the API
```bash
python3 test_api.py
```

### Manual Installation
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Environment Configuration

Edit the `.env` file with your Sinch API credentials:

```bash
# Sinch API Configuration
SINCH_ACCESS_KEY=your_actual_access_key
SINCH_ACCESS_SECRET=your_actual_access_secret
SINCH_PROJECT_ID=your_actual_project_id

# Fax Configuration
PHARMACY_FAX_NUMBER=17057415595

# PDF Configuration
PDF_SAVE_DIR=generated_pdfs

# Optional Callback URL
CALLBACK_URL=https://your-domain.com/fax-callback
```

## URLs After Starting

- **API Documentation**: http://localhost:8000/docs
- **Test Form**: http://localhost:8000/static/test_form.html
- **Health Check**: http://localhost:8000/
- **Generate PDF Only**: POST http://localhost:8000/generate-pdf
- **Send Fax**: POST http://localhost:8000/send-fax
- **Fax Status**: GET http://localhost:8000/fax-status/{fax_id}

## Production Deployment

### Heroku
```bash
# Install Heroku CLI first
heroku create your-app-name
heroku config:set SINCH_ACCESS_KEY=your_key
heroku config:set SINCH_ACCESS_SECRET=your_secret
heroku config:set SINCH_PROJECT_ID=your_project_id
git add .
git commit -m "Initial commit"
git push heroku main
```

### Railway
```bash
# Connect GitHub repo to Railway
# Set environment variables in Railway dashboard
# Deploy automatically
```

### Docker
```bash
# Build Docker image
docker build -t webflow-fax-api .

# Run container
docker run -p 8000:8000 --env-file .env webflow-fax-api
```

## Troubleshooting

### Python Not Found
```bash
# Install Python 3.8+
brew install python3  # macOS
sudo apt install python3 python3-pip  # Ubuntu
```

### Permission Denied
```bash
chmod +x build.sh start.sh
```

### Port Already in Use
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Missing Dependencies
```bash
# Rebuild
./build.sh
```

## File Structure
```
webflow-form/
├── main.py              # FastAPI application
├── pdf_generator.py     # PDF generation module
├── fax_sender.py        # Sinch fax integration
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── Procfile            # Heroku deployment
├── build.sh            # Build script
├── start.sh            # Start script
├── test_api.py         # API test script
├── test_form.html      # HTML test form
├── env.example         # Environment template
├── .env                # Your environment variables
└── generated_pdfs/     # Generated PDF files
```
