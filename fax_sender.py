"""
Fax sending module for transmitting PDFs via Sinch API.
"""
import requests
import os
import mimetypes
from typing import Dict, Any, Optional
from config import (
    SINCH_ACCESS_KEY, 
    SINCH_ACCESS_SECRET, 
    SINCH_PROJECT_ID,
    SINCH_FAX_API_URL,
    SINCH_MEDIA_API_URL,
    CALLBACK_URL
)


class FaxSender:
    """Handles sending PDFs via fax using Sinch API."""
    
    def __init__(self, access_key: str = None, access_secret: str = None, project_id: str = None):
        """
        Initialize fax sender.
        
        Args:
            access_key: Sinch access key (optional, uses config default)
            access_secret: Sinch access secret (optional, uses config default)
            project_id: Sinch project ID (optional, uses config default)
        """
        self.access_key = access_key or SINCH_ACCESS_KEY
        self.access_secret = access_secret or SINCH_ACCESS_SECRET
        self.project_id = project_id or SINCH_PROJECT_ID
        self.fax_api_url = f"{SINCH_FAX_API_URL}/{self.project_id}/faxes"
        self.media_api_url = f"{SINCH_MEDIA_API_URL}/{self.project_id}/media"
    
    def upload_file_to_sinch(self, file_path: str) -> Dict[str, Any]:
        """
        Upload file to Sinch media service and get content URL.
        
        Args:
            file_path: Path to the file to upload
            
        Returns:
            Dictionary with upload result and content URL
        """
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }
        
        try:
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/pdf"
            
            # Prepare headers
            headers = {
                "Content-Type": mime_type
            }
            
            # Read file content
            with open(file_path, "rb") as f:
                file_content = f.read()
            
            # Upload to Sinch media service
            response = requests.post(
                self.media_api_url,
                headers=headers,
                data=file_content,
                auth=(self.access_key, self.access_secret)
            )
            
            if response.status_code == 201:
                data = response.json()
                return {
                    "success": True,
                    "content_url": data.get("url"),
                    "media_id": data.get("id")
                }
            else:
                return {
                    "success": False,
                    "error": f"Upload failed: {response.status_code} - {response.text}"
                }
                
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Network error during upload: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error during upload: {str(e)}"
            }

    def send_pdf_as_fax(self, pdf_path: str, fax_number: str, filename: str = "document.pdf", content_url: str = None) -> Dict[str, Any]:
        """
        Send PDF file as fax using Sinch API.
        
        Args:
            pdf_path: Path to the PDF file
            fax_number: Destination fax number
            filename: Name for the fax file
            content_url: Optional pre-uploaded content URL (if None, will upload file)
            
        Returns:
            Dictionary with response status and details
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: For other fax sending errors
        """
        if not content_url and not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            # If no content URL provided, upload the file first
            if not content_url:
                upload_result = self.upload_file_to_sinch(pdf_path)
                if not upload_result["success"]:
                    return {
                        "success": False,
                        "error": f"File upload failed: {upload_result['error']}",
                        "fax_number": fax_number,
                        "filename": filename
                    }
                content_url = upload_result["content_url"]
            
            # Prepare fax payload
            payload = {
                "to": fax_number,
                "contentUrl": content_url
            }
            
            # Add callback URL if configured
            if CALLBACK_URL:
                payload["callbackUrl"] = CALLBACK_URL
            
            # Prepare headers
            headers = {
                "Content-Type": "application/json"
            }
            
            # Send fax request
            response = requests.post(
                self.fax_api_url,
                json=payload,
                headers=headers,
                auth=(self.access_key, self.access_secret)
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "fax_id": data.get("id"),
                    "response_data": data,
                    "fax_number": fax_number,
                    "filename": filename,
                    "content_url": content_url
                }
            else:
                return {
                    "success": False,
                    "error": f"Fax request failed: {response.status_code} - {response.text}",
                    "fax_number": fax_number,
                    "filename": filename
                }
            
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "fax_number": fax_number,
                "filename": filename
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "fax_number": fax_number,
                "filename": filename
            }
    
    def cleanup_temp_file(self, file_path: str):
        """
        Clean up temporary file if it exists.
        
        Args:
            file_path: Path to file to delete
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Could not delete temporary file {file_path}: {e}")
    
    def validate_fax_number(self, fax_number: str) -> bool:
        """
        Basic validation for fax number format.
        
        Args:
            fax_number: Fax number to validate
            
        Returns:
            True if valid format, False otherwise
        """
        if not fax_number:
            return False
        
        # Remove any non-digit characters
        clean_number = ''.join(filter(str.isdigit, fax_number))
        
        # Check if it's a reasonable length (7-15 digits)
        return 7 <= len(clean_number) <= 15
    
    def get_fax_status(self, fax_id: str) -> Dict[str, Any]:
        """
        Get the status of a sent fax.
        
        Args:
            fax_id: The ID of the fax to check
            
        Returns:
            Dictionary with fax status information
        """
        try:
            url = f"{self.fax_api_url}/{fax_id}"
            
            response = requests.get(
                url,
                auth=(self.access_key, self.access_secret)
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "fax_status": data
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to get fax status: {response.status_code} - {response.text}"
                }
                
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
