# Webflow Integration Guide

This guide shows you how to integrate your form-to-fax API with Webflow forms.

## Method 1: Using Webflow's Form Submission Webhook

### Step 1: Set up your API endpoint
Your API should be accessible via HTTPS. For production, you'll need to deploy it to a service like:
- Heroku
- Railway
- DigitalOcean App Platform
- AWS Lambda
- Google Cloud Run

### Step 2: Configure Webflow Form

1. **In Webflow Designer:**
   - Go to your form element
   - Click on the form settings
   - Scroll to "Form Settings"
   - Enable "Form Submission"

2. **Configure Form Fields:**
   Make sure your form field names match the expected API format:
   ```
   OR-Name (for first name)
   OR-Last-name (for last name)  
   OR-Phone-number (for phone)
   OR-Medication (for medications)
   OR-note (for notes)
   delivery_option (for delivery option)
   address (for address)
   time_slot (for time slot)
   ```

3. **Set up Form Submission Action:**
   - Choose "Custom Code"
   - Add this JavaScript:

```javascript
// Webflow Form Integration
document.addEventListener('DOMContentLoaded', function() {
  // Find your form (adjust selector as needed)
  const form = document.querySelector('#your-form-id');
  
  if (form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault(); // Prevent default form submission
      
      // Show loading state
      const submitButton = form.querySelector('input[type="submit"]');
      const originalText = submitButton.value;
      submitButton.value = 'Sending...';
      submitButton.disabled = true;
      
      try {
        // Collect form data
        const formData = new FormData(form);
        const data = {};
        
        // Map form fields to API format
        formData.forEach((value, key) => {
          data[key] = value;
        });
        
        // Send to your API
        const response = await fetch('https://your-api-domain.com/send-fax', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok && result.status === 'success') {
          // Success - show success message
          showMessage('✅ PDF generated and fax sent successfully!', 'success');
          
          // Optional: Redirect or reset form
          form.reset();
        } else {
          // Error - show error message
          showMessage('❌ Error: ' + (result.message || 'Failed to send fax'), 'error');
        }
        
      } catch (error) {
        console.error('Error:', error);
        showMessage('❌ Network error. Please try again.', 'error');
      } finally {
        // Reset button state
        submitButton.value = originalText;
        submitButton.disabled = false;
      }
    });
  }
});

// Function to show messages to user
function showMessage(message, type) {
  // Create or find message container
  let messageContainer = document.querySelector('#form-message');
  if (!messageContainer) {
    messageContainer = document.createElement('div');
    messageContainer.id = 'form-message';
    messageContainer.style.cssText = `
      padding: 15px;
      margin: 10px 0;
      border-radius: 5px;
      font-weight: bold;
    `;
    
    // Insert after form
    const form = document.querySelector('#your-form-id');
    form.parentNode.insertBefore(messageContainer, form.nextSibling);
  }
  
  // Set message content and style
  messageContainer.textContent = message;
  messageContainer.style.backgroundColor = type === 'success' ? '#d4edda' : '#f8d7da';
  messageContainer.style.color = type === 'success' ? '#155724' : '#721c24';
  messageContainer.style.border = type === 'success' ? '1px solid #c3e6cb' : '1px solid #f5c6cb';
  
  // Auto-hide after 5 seconds
  setTimeout(() => {
    messageContainer.style.display = 'none';
  }, 5000);
}
```

## Method 2: Using Zapier Integration

### Step 1: Create Zapier Webhook

1. **Go to Zapier.com**
2. **Create a new Zap**
3. **Choose "Webflow" as trigger**
4. **Select "New Form Submission"**
5. **Connect your Webflow account**
6. **Choose your form**

### Step 2: Set up Action

1. **Choose "Webhooks by Zapier" as action**
2. **Select "POST"**
3. **Configure the webhook:**
   - **URL:** `https://your-api-domain.com/send-fax`
   - **Method:** POST
   - **Headers:** `Content-Type: application/json`
   - **Body:** Map Webflow fields to your API format

```json
{
  "OR-Name": "{{first_name}}",
  "OR-Last-name": "{{last_name}}",
  "OR-Phone-number": "{{phone}}",
  "OR-Medication": "{{medication}}",
  "OR-note": "{{notes}}",
  "delivery_option": "{{delivery_option}}",
  "address": "{{address}}",
  "time_slot": "{{time_slot}}"
}
```

## Method 3: Using Webflow's Native Form Settings

### Step 1: Configure Form in Webflow

1. **In Webflow Designer:**
   - Select your form
   - Go to Form Settings
   - Set "Form Submission" to "Webhook"

2. **Add Webhook URL:**
   ```
   https://your-api-domain.com/send-fax
   ```

3. **Configure Headers:**
   ```
   Content-Type: application/json
   ```

### Step 2: Test the Integration

Use this test script to verify everything works:

```bash
# Run the test script
python3 test_api.py
```

## Testing Your Integration

### 1. Test Locally First

```bash
# Start your API server
cd /Users/muhammadshahidsharif/Documents/webflow-form
python3 -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)"

# In another terminal, run the test
python3 test_api.py
```

### 2. Test with Real Webflow Form

1. **Create a simple test form in Webflow**
2. **Use Method 1 (Custom Code) for testing**
3. **Submit the form and check:**
   - API receives the data
   - PDF is generated
   - Fax is sent (if Sinch is configured)

## Production Deployment

### For Heroku:

1. **Create Procfile:**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. **Deploy:**
```bash
git add .
git commit -m "Add Sinch integration"
git push heroku main
```

3. **Set Environment Variables:**
```bash
heroku config:set SINCH_ACCESS_KEY=your_key
heroku config:set SINCH_ACCESS_SECRET=your_secret
heroku config:set SINCH_PROJECT_ID=your_project_id
```

### For Railway:

1. **Connect your GitHub repo**
2. **Set environment variables in Railway dashboard**
3. **Deploy automatically**

## Common Issues & Solutions

### Issue 1: CORS Errors
Add CORS middleware to your FastAPI app:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 2: Form Field Mapping
Make sure Webflow form field names exactly match your API expectations:
- Use `name="OR-Name"` in Webflow
- Check field names in browser dev tools

### Issue 3: HTTPS Requirements
- Webflow requires HTTPS for webhooks
- Use services like ngrok for local testing:
```bash
ngrok http 8000
```

## Form Field Reference

Your API expects these field names:

| Webflow Field Name | Description | Required |
|-------------------|-------------|----------|
| `OR-Name` | First name | Yes |
| `OR-Last-name` | Last name | Yes |
| `OR-Phone-number` | Phone number | Yes |
| `OR-Medication` | Medications (comma-separated) | Yes |
| `OR-note` | Special notes | No |
| `delivery_option` | Delivery or pickup | No |
| `address` | Delivery address | No |
| `time_slot` | Preferred time slot | No |

## Success Response Format

When successful, your API returns:
```json
{
  "status": "success",
  "message": "PDF generated and fax sent successfully",
  "fax_id": "fax_12345",
  "fax_number": "17057415595",
  "response_data": {...}
}
```

## Error Response Format

When there's an error:
```json
{
  "status": "error",
  "message": "Error description"
}
```
