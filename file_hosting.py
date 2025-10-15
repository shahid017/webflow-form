"""
File hosting utilities for making PDFs publicly accessible for Sinch fax API.
"""
import requests
import os
import tempfile
from typing import Dict, Any, Optional

class FileHostingService:
    """Service to make PDFs publicly accessible for fax sending."""
    
    def __init__(self):
        self.service_name = "file.io"  # Free temporary file hosting
    
    def upload_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Upload PDF to a temporary public hosting service.
        
        Args:
            pdf_path: Path to the PDF file to upload
            
        Returns:
            Dictionary with upload result and public URL
        """
        if not os.path.exists(pdf_path):
            return {
                "success": False,
                "error": f"PDF file not found: {pdf_path}"
            }
        
        try:
            with open(pdf_path, 'rb') as file:
                files = {'file': file}
                
                # Upload to file.io (free temporary hosting)
                response = requests.post('https://file.io', files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        return {
                            "success": True,
                            "public_url": data.get('link'),
                            "file_id": data.get('key'),
                            "expires": data.get('expiry')
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Upload failed: {data.get('error', 'Unknown error')}"
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
    
    def upload_to_github_gist(self, pdf_path: str, filename: str = "document.pdf") -> Dict[str, Any]:
        """
        Alternative: Upload to GitHub Gist as a public file.
        Note: This requires a GitHub token and creates a gist.
        """
        # This would require GitHub API token
        # For now, we'll use file.io which is simpler
        return self.upload_pdf(pdf_path)

# Alternative simple solution: Use a different free hosting service
class SimpleFileHost:
    """Simple file hosting using multiple services as fallback."""
    
    def upload_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Try multiple services to upload PDF."""
        
        services = [
            self._try_fileio,
            self._try_transfer_sh,
        ]
        
        for service in services:
            try:
                result = service(pdf_path)
                if result["success"]:
                    return result
            except Exception as e:
                print(f"Service failed: {e}")
                continue
        
        return {
            "success": False,
            "error": "All file hosting services failed"
        }
    
    def _try_fileio(self, pdf_path: str) -> Dict[str, Any]:
        """Try file.io service."""
        with open(pdf_path, 'rb') as file:
            files = {'file': file}
            response = requests.post('https://file.io', files=files, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return {
                        "success": True,
                        "public_url": data.get('link'),
                        "service": "file.io"
                    }
        
        return {"success": False, "error": "file.io failed"}
    
    def _try_transfer_sh(self, pdf_path: str) -> Dict[str, Any]:
        """Try transfer.sh service."""
        filename = os.path.basename(pdf_path)
        with open(pdf_path, 'rb') as file:
            response = requests.put(
                f'https://transfer.sh/{filename}',
                data=file,
                headers={'Max-Downloads': '1', 'Max-Days': '1'},
                timeout=30
            )
            
            if response.status_code == 200:
                url = response.text.strip()
                return {
                    "success": True,
                    "public_url": url,
                    "service": "transfer.sh"
                }
        
        return {"success": False, "error": "transfer.sh failed"}
