# 🚀 Render.com Deployment Guide

## The Issue You're Seeing

The error message indicates that Render can't detect an open port on `0.0.0.0`. This happens because:

1. Your app is binding to `127.0.0.1:8000` instead of `0.0.0.0:$PORT`
2. Render expects apps to use the `$PORT` environment variable
3. The app needs to bind to `0.0.0.0` to be accessible from outside

## ✅ Solution

I've created the necessary files to fix this:

### 1. Updated Procfile
```bash
web: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
```

### 2. Created render.yaml
This provides Render with deployment configuration.

### 3. Created main_render.py
This is a Render-optimized version of your main.py with:
- Proper port binding
- CORS middleware for Webflow
- Health check endpoint

## 🔧 Quick Fix

### Option 1: Update your current main.py

Add this to the end of your `main.py`:

```python
# For Render deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### Option 2: Use the optimized version

Replace your `main.py` with `main_render.py`:

```bash
mv main.py main_backup.py
mv main_render.py main.py
```

## 🌐 Deploy to Render

### Step 1: Connect Repository
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Choose "Web Service"

### Step 2: Configure Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Python Version**: 3.9 or higher

### Step 3: Set Environment Variables
In Render dashboard, add these environment variables:

```
SINCH_ACCESS_KEY=your_actual_access_key
SINCH_ACCESS_SECRET=your_actual_access_secret
SINCH_PROJECT_ID=your_actual_project_id
PHARMACY_FAX_NUMBER=17057415595
PDF_SAVE_DIR=generated_pdfs
CALLBACK_URL=https://your-domain.com/fax-callback
```

### Step 4: Deploy
Click "Create Web Service" and Render will:
1. Build your application
2. Install dependencies
3. Start the server on the correct port
4. Make it accessible via HTTPS

## 🧪 Test Your Deployment

After deployment, test these endpoints:

```bash
# Health check
curl https://your-app-name.onrender.com/

# API documentation
https://your-app-name.onrender.com/docs

# Test fax endpoint
curl -X POST https://your-app-name.onrender.com/send-fax \
  -H "Content-Type: application/json" \
  -d '{
    "OR-Name": "Test",
    "OR-Last-name": "User",
    "OR-Phone-number": "123-456-7890",
    "OR-Medication": "Test medication"
  }'
```

## 🔧 Webflow Integration

Once deployed, update your Webflow JavaScript with the Render URL:

```javascript
const response = await fetch('https://your-app-name.onrender.com/send-fax', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
});
```

## 🚨 Common Issues

### Port Binding Error
- ✅ Fixed by using `0.0.0.0:$PORT` in start command
- ✅ Fixed by binding to `0.0.0.0` instead of `127.0.0.1`

### CORS Issues
- ✅ Fixed by adding CORS middleware in main_render.py

### Environment Variables
- ✅ Make sure all Sinch credentials are set in Render dashboard

### Cold Start
- ✅ Render has cold start delays for free tier
- ✅ Consider upgrading to paid tier for production

## 📋 Files Created

- `render.yaml` - Render deployment configuration
- `main_render.py` - Render-optimized main application
- `RENDER_DEPLOYMENT.md` - This deployment guide

## 🎯 Next Steps

1. **Commit and push** your changes to GitHub
2. **Connect repository** to Render
3. **Set environment variables** in Render dashboard
4. **Deploy** and get your HTTPS URL
5. **Update Webflow** with the new API URL
6. **Test** the integration

Your app should now work properly on Render! 🚀
