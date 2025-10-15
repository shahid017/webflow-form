"""
Configuration settings for the Webflow form to fax application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Sinch API Configuration
SINCH_ACCESS_KEY = os.getenv("SINCH_ACCESS_KEY")
SINCH_ACCESS_SECRET = os.getenv("SINCH_ACCESS_SECRET")
SINCH_PROJECT_ID = os.getenv("SINCH_PROJECT_ID")
PHARMACY_FAX_NUMBER = os.getenv("PHARMACY_FAX_NUMBER", "17057415595")

# Validate required environment variables
def validate_config():
    """Validate that all required environment variables are set"""
    required_vars = {
        "SINCH_ACCESS_KEY": SINCH_ACCESS_KEY,
        "SINCH_ACCESS_SECRET": SINCH_ACCESS_SECRET,
        "SINCH_PROJECT_ID": SINCH_PROJECT_ID,
    }
    
    missing_vars = []
    for var_name, var_value in required_vars.items():
        if not var_value:
            missing_vars.append(var_name)
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}. "
            f"Please create a .env file with these variables."
        )

# Validate configuration on import
validate_config()

# PDF Configuration
PDF_FILENAME_PREFIX = "refill_order"
PDF_SAVE_DIR = os.getenv("PDF_SAVE_DIR", "generated_pdfs")

# Sinch API URLs
SINCH_FAX_API_URL = "https://fax.api.sinch.com/v3/projects"
SINCH_MEDIA_API_URL = "https://media.api.sinch.com/v1/projects"

# File Upload Configuration
UPLOAD_ENABLED = os.getenv("UPLOAD_ENABLED", "true").lower() == "true"
CALLBACK_URL = os.getenv("CALLBACK_URL", "")  # Optional callback URL for fax status
