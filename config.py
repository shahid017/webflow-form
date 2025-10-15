"""
Configuration settings for the Webflow form to fax application.
"""
import os

# Sinch API Configuration
SINCH_ACCESS_KEY = os.getenv("SINCH_ACCESS_KEY", "ecb77cdc-0db0-441b-83c9-8a362de5cb22")
SINCH_ACCESS_SECRET = os.getenv("SINCH_ACCESS_SECRET", "2Pryq7RuJ7u6dmB2MEyz2mzJZQ")
SINCH_PROJECT_ID = os.getenv("SINCH_PROJECT_ID", "d04cbbec-47c1-4f6a-b573-81405882ab52")
PHARMACY_FAX_NUMBER = os.getenv("PHARMACY_FAX_NUMBER", "+17057415595")

# PDF Configuration
PDF_FILENAME_PREFIX = "refill_order"
PDF_SAVE_DIR = os.getenv("PDF_SAVE_DIR", "generated_pdfs")

# Sinch API URLs
SINCH_FAX_API_URL = "https://fax.api.sinch.com/v3/projects"
SINCH_MEDIA_API_URL = "https://media.api.sinch.com/v1/projects"

# File Upload Configuration
UPLOAD_ENABLED = os.getenv("UPLOAD_ENABLED", "true").lower() == "true"
CALLBACK_URL = os.getenv("CALLBACK_URL", "")  # Optional callback URL for fax status
