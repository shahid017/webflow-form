# Webflow Form to Fax API

This application receives form data from Webflow, generates a PDF, and sends it as a fax using the Sinch API.

## Project Structure

The application has been modularized into separate components:

- **`main.py`** - FastAPI application with endpoints
- **`pdf_generator.py`** - Handles PDF generation from form data
- **`fax_sender.py`** - Handles fax transmission via Sinch API
- **`config.py`** - Configuration settings and environment variables

## API Endpoints

### 1. `/send-fax` (POST)
- **Purpose**: Complete workflow - receives form data, generates PDF, and sends as fax
- **Input**: JSON with form fields
- **Output**: Success/error status with fax response

### 2. `/generate-pdf` (POST)
- **Purpose**: Generate PDF from form data only (no fax sending)
- **Input**: JSON with form fields
- **Output**: Success status with PDF file path

### 3. `/send-fax-from-file` (POST)
- **Purpose**: Send an existing PDF file as fax
- **Input**: JSON with `pdf_path`, `fax_number`, and `filename`
- **Output**: Success/error status with fax response

### 4. `/fax-status/{fax_id}` (GET)
- **Purpose**: Check the status of a sent fax
- **Input**: Fax ID as URL parameter
- **Output**: Current fax status and details

## Configuration

Set the following environment variables:

```bash
SINCH_ACCESS_KEY=your_sinch_access_key
SINCH_ACCESS_SECRET=your_sinch_access_secret
SINCH_PROJECT_ID=your_sinch_project_id
PHARMACY_FAX_NUMBER=17057415595
PDF_SAVE_DIR=generated_pdfs
CALLBACK_URL=https://your-domain.com/fax-callback  # Optional
```

**Getting Sinch Credentials:**
1. Go to [dashboard.sinch.com](https://dashboard.sinch.com)
2. Navigate to Settings > Access Keys
3. Copy your access key, secret, and project ID

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables (see Configuration section)

3. Run the application:
```bash
uvicorn main:app --reload
```

## Usage

### Generate PDF and Send Fax
```bash
curl -X POST "http://localhost:8000/send-fax" \
     -H "Content-Type: application/json" \
     -d '{
       "OR-Name": "John",
       "OR-Last-name": "Doe",
       "OR-Phone-number": "123-456-7890",
       "OR-Medication": "Aspirin, Ibuprofen",
       "delivery_option": "Delivery",
       "address": "123 Main St",
       "time_slot": "2-4 PM"
     }'
```

### Generate PDF Only
```bash
curl -X POST "http://localhost:8000/generate-pdf" \
     -H "Content-Type: application/json" \
     -d '{
       "OR-Name": "John",
       "OR-Last-name": "Doe",
       "OR-Phone-number": "123-456-7890",
       "OR-Medication": "Aspirin, Ibuprofen"
     }'
```

### Send Existing PDF as Fax
```bash
curl -X POST "http://localhost:8000/send-fax-from-file" \
     -H "Content-Type: application/json" \
     -d '{
       "pdf_path": "/path/to/document.pdf",
       "fax_number": "17057415595",
       "filename": "document.pdf"
     }'
```

### Check Fax Status
```bash
curl -X GET "http://localhost:8000/fax-status/{fax_id}"
```

## Features

- **Modular Design**: Separate concerns for PDF generation and fax sending
- **Sinch Integration**: Uses Sinch API for reliable fax transmission
- **File Upload**: Automatic file upload to Sinch media service
- **Error Handling**: Comprehensive error handling and validation
- **Flexible**: Can generate PDFs without sending fax, or send existing PDFs
- **Configuration**: Environment-based configuration for easy deployment
- **File Management**: Automatic cleanup of temporary files
- **Validation**: Fax number format validation
- **Status Tracking**: Check fax delivery status via API
- **Callback Support**: Optional callback URL for fax status updates
