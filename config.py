"""
Configuration settings for the Webflow form to fax application.
"""
import os

# Sinch API Configuration
SINCH_ACCESS_KEY = os.getenv("SINCH_ACCESS_KEY", "YOUR_access_key")
SINCH_ACCESS_SECRET = os.getenv("SINCH_ACCESS_SECRET", "YOUR_access_secret")
SINCH_PROJECT_ID = os.getenv("SINCH_PROJECT_ID", "YOUR_project_id")
PHARMACY_FAX_NUMBER = os.getenv("PHARMACY_FAX_NUMBER", "17057415595")

# PDF Configuration
PDF_FILENAME_PREFIX = "refill_order"
PDF_SAVE_DIR = os.getenv("PDF_SAVE_DIR", "generated_pdfs")

# Sinch API URLs
SINCH_FAX_API_URL = "https://fax.api.sinch.com/v3/projects"
SINCH_MEDIA_API_URL = "https://media.api.sinch.com/v1/projects"

# File Upload Configuration
UPLOAD_ENABLED = os.getenv("UPLOAD_ENABLED", "true").lower() == "true"
CALLBACK_URL = os.getenv("CALLBACK_URL", "")  # Optional callback URL for fax status
