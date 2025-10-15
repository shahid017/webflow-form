"""
Simple file server to temporarily serve PDFs for fax sending.
"""
import http.server
import socketserver
import threading
import os
import time
from urllib.parse import urlparse

class PDFFileServer:
    """Simple HTTP server to serve PDFs temporarily."""
    
    def __init__(self, port=8080):
        self.port = port
        self.server = None
        self.server_thread = None
        self.base_url = f"http://localhost:{port}"
    
    def start_server(self):
        """Start the HTTP server in a background thread."""
        try:
            handler = http.server.SimpleHTTPRequestHandler
            self.server = socketserver.TCPServer(("", self.port), handler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            print(f"📡 File server started on {self.base_url}")
            return True
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the HTTP server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("🛑 File server stopped")
    
    def get_pdf_url(self, pdf_path):
        """Get the public URL for a PDF file."""
        if not os.path.exists(pdf_path):
            return None
        
        filename = os.path.basename(pdf_path)
        return f"{self.base_url}/{filename}"

# Global server instance
pdf_server = None

def start_pdf_server():
    """Start the PDF server."""
    global pdf_server
    pdf_server = PDFFileServer()
    return pdf_server.start_server()

def stop_pdf_server():
    """Stop the PDF server."""
    global pdf_server
    if pdf_server:
        pdf_server.stop_server()

def get_pdf_url(pdf_path):
    """Get public URL for a PDF."""
    global pdf_server
    if pdf_server:
        return pdf_server.get_pdf_url(pdf_path)
    return None
