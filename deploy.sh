#!/bin/bash

# Deploy to Render script

echo "🚀 Deploying to Render..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Fix API documentation with Pydantic models

- Added Pydantic models for proper API documentation
- Fixed 'No parameters' issue in /docs
- Added proper field validation and examples
- Improved API documentation with detailed descriptions
- Added response models for consistent API responses"

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  No remote origin found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/yourusername/your-repo.git"
    echo "   git push -u origin main"
    exit 1
fi

# Push to GitHub (which will trigger Render deployment)
echo "🌐 Pushing to GitHub..."
git push origin main

echo "✅ Deployment initiated!"
echo "📋 Check your Render dashboard for deployment status"
echo "🔗 Your API docs will be available at: https://webflow-form.onrender.com/docs"
echo ""
echo "🧪 Test the updated API documentation:"
echo "   curl https://webflow-form.onrender.com/docs"
