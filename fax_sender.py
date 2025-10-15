"""
Fax sending module for transmitting PDFs via Sinch API.
"""
import requests
import os
import base64
from typing import Dict, Any, Optional
from config import (
    SINCH_ACCESS_KEY, 
    SINCH_ACCESS_SECRET, 
    SINCH_PROJECT_ID,
    SINCH_FAX_API_URL,
    CALLBACK_URL
)
from file_hosting import SimpleFileHost


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
        self.file_host = SimpleFileHost()
    
    def send_pdf_as_fax(self, pdf_path: str, fax_number: str, filename: str = "document.pdf") -> Dict[str, Any]:
        """
        Send PDF file as fax using Sinch API.
        
        This uploads the generated PDF to a public hosting service and then sends it via fax.
        
        Args:
            pdf_path: Path to the PDF file to send
            fax_number: Destination fax number
            filename: Name for the fax file
            
        Returns:
            Dictionary with response status and details
        """
        try:
            # Check if PDF file exists
            if not os.path.exists(pdf_path):
                return {
                    "success": False,
                    "error": f"PDF file not found: {pdf_path}",
                    "fax_number": fax_number,
                    "filename": filename
                }
            
            print(f"📄 Uploading PDF to public hosting service...")
            print(f"📁 PDF path: {pdf_path}")
            
            # Upload PDF to get a public URL
            upload_result = self.file_host.upload_pdf(pdf_path)
            
            if not upload_result["success"]:
                return {
                    "success": False,
                    "error": f"Failed to upload PDF: {upload_result['error']}",
                    "fax_number": fax_number,
                    "filename": filename
                }
            
            content_url = upload_result["public_url"]
            print(f"✅ PDF uploaded successfully!")
            print(f"🔗 Public URL: {content_url}")
            
            # Create basic auth header
            credentials = f"{self.access_key}:{self.access_secret}"
            encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
            
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
                'Content-Type': 'application/json',
                'Authorization': f'Basic {encoded_credentials}'
            }
            
            print(f"📤 Sending fax to {fax_number}...")
            print(f"🔗 Using content URL: {content_url}")
            print(f"📋 Payload: {payload}")
            
            # Send fax request
            response = requests.post(
                self.fax_api_url,
                headers=headers,
                json=payload
            )
            
            print(f"📡 Response status: {response.status_code}")
            print(f"📄 Response text: {response.text}")
            
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
    
    def send_pdf_with_url(self, pdf_url: str, fax_number: str, filename: str = "document.pdf") -> Dict[str, Any]:
        """
        Send PDF via fax using a public URL.
        
        Args:
            pdf_url: Public URL to the PDF file
            fax_number: Destination fax number
            filename: Name for the fax file
            
        Returns:
            Dictionary with response status and details
        """
        try:
            # Create basic auth header
            credentials = f"{self.access_key}:{self.access_secret}"
            encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
            
            # Prepare fax payload
            payload = {
                "to": fax_number,
                "contentUrl": pdf_url
            }
            
            # Add callback URL if configured
            if CALLBACK_URL:
                payload["callbackUrl"] = CALLBACK_URL
            
            # Prepare headers
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {encoded_credentials}'
            }
            
            print(f"📤 Sending fax to {fax_number}...")
            print(f"🔗 Using PDF URL: {pdf_url}")
            print(f"📋 Payload: {payload}")
            
            # Send fax request
            response = requests.post(
                self.fax_api_url,
                headers=headers,
                json=payload
            )
            
            print(f"📡 Response status: {response.status_code}")
            print(f"📄 Response text: {response.text}")
            
            if response.status_code in [200, 201]:
                data = response.json()
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "fax_id": data.get("id"),
                    "response_data": data,
                    "fax_number": fax_number,
                    "filename": filename,
                    "content_url": pdf_url
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
