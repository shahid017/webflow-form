# Load environment variables from .env file FIRST
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import os
import tempfile
from pdf_generator import generate_pdf
from fax_sender import FaxSender
from config import PHARMACY_FAX_NUMBER
from models import FormData, SendFaxFromFileRequest, ApiResponse, HealthResponse

app = FastAPI(
    title="Webflow Form to Fax API",
    description="API to receive form data from Webflow and send it as fax via Sinch",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize services
fax_sender = FaxSender()

# Store temporary PDFs for serving
temp_pdfs = {}

@app.get("/pdf/{pdf_id}")
async def serve_pdf(pdf_id: str):
    """Serve a PDF file by ID."""
    if pdf_id in temp_pdfs:
        pdf_path = temp_pdfs[pdf_id]
        if os.path.exists(pdf_path):
            return FileResponse(
                pdf_path,
                media_type="application/pdf",
                filename=f"prescription_{pdf_id}.pdf"
            )
    
    raise HTTPException(status_code=404, detail="PDF not found")

@app.post("/send-fax", response_model=ApiResponse)
async def send_fax(form_data: FormData):
    """
    Endpoint to receive form data, generate PDF, and send it as fax.
    
    This endpoint accepts form data from Webflow, generates a PDF document,
    and sends it as a fax using the Sinch API.
    """
    try:
        # Convert Pydantic model to dict using field aliases
        data = form_data.dict(by_alias=True)
        
        # Step 1: Generate PDF from form data
        import uuid
        pdf_id = str(uuid.uuid4())[:8]  # Short unique ID
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            pdf_path = generate_pdf(data, temp_file.name)
        
        # Store PDF for serving
        temp_pdfs[pdf_id] = pdf_path
        
        # Step 2: Create public URL for the PDF
        # In production, this would be your actual domain
        base_url = "https://webflow-form.onrender.com"  # Your Render URL
        pdf_url = f"{base_url}/pdf/{pdf_id}"
        
        # Step 3: Send PDF as fax using the public URL
        fax_result = fax_sender.send_pdf_with_url(
            pdf_url=pdf_url,
            fax_number=PHARMACY_FAX_NUMBER,
            filename="refill_order.pdf"
        )
        
        # Step 4: Clean up temporary file after some delay
        # (Give time for fax to be sent)
        import threading
        def cleanup_later():
            import time
            time.sleep(300)  # Wait 5 minutes
            if pdf_id in temp_pdfs:
                fax_sender.cleanup_temp_file(temp_pdfs[pdf_id])
                del temp_pdfs[pdf_id]
        
        threading.Thread(target=cleanup_later, daemon=True).start()
        
        if fax_result["success"]:
            return ApiResponse(
                status="success",
                message="PDF generated and fax sent successfully",
                fax_id=fax_result.get("fax_id"),
                fax_number=fax_result["fax_number"],
                response_data=fax_result["response_data"]
            )
        else:
            return ApiResponse(
                status="error",
                message="PDF generated but fax failed",
                error=fax_result["error"]
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-pdf", response_model=ApiResponse)
async def generate_pdf_only(form_data: FormData):
    """
    Endpoint to generate PDF from form data without sending fax.
    
    Useful for testing or when you only need the PDF document.
    The PDF will be saved permanently in the generated_pdfs directory.
    """
    try:
        # Convert Pydantic model to dict using field aliases
        data = form_data.dict(by_alias=True)
        
        # Generate PDF and save permanently
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data.get('OR-Name', 'Unknown')}_{data.get('OR-Last-name', 'User')}_{timestamp}.pdf"
        pdf_path = generate_pdf(data, filename)
        
        return ApiResponse(
            status="success",
            message="PDF generated successfully",
            pdf_path=pdf_path
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/send-fax-from-file", response_model=ApiResponse)
async def send_fax_from_file(request_data: SendFaxFromFileRequest):
    """
    Endpoint to send an existing PDF file as fax.
    
    This endpoint allows you to send a previously generated PDF file
    as a fax without regenerating it.
    """
    try:
        # Validate fax number
        if not fax_sender.validate_fax_number(request_data.fax_number):
            raise HTTPException(status_code=400, detail="Invalid fax number format")
        
        # Send fax
        fax_result = fax_sender.send_pdf_as_fax(
            request_data.pdf_path, 
            request_data.fax_number, 
            request_data.filename
        )
        
        if fax_result["success"]:
            return ApiResponse(
                status="success",
                message="Fax sent successfully",
                fax_id=fax_result.get("fax_id"),
                fax_number=fax_result["fax_number"],
                response_data=fax_result["response_data"]
            )
        else:
            return ApiResponse(
                status="error",
                message="Fax sending failed",
                error=fax_result["error"]
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fax-status/{fax_id}", response_model=ApiResponse)
async def get_fax_status(fax_id: str):
    """
    Endpoint to check the status of a sent fax.
    
    Use this endpoint to check the delivery status of a previously sent fax.
    The fax_id is returned when you send a fax via the /send-fax endpoint.
    """
    try:
        status_result = fax_sender.get_fax_status(fax_id)
        
        if status_result["success"]:
            return ApiResponse(
                status="success",
                message="Fax status retrieved successfully",
                response_data=status_result["fax_status"]
            )
        else:
            return ApiResponse(
                status="error",
                message="Failed to get fax status",
                error=status_result["error"]
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Webflow Form to Fax API is running",
        version="1.0.0",
        endpoints={
            "docs": "/docs",
            "send_fax": "/send-fax",
            "generate_pdf": "/generate-pdf",
            "send_fax_from_file": "/send-fax-from-file",
            "fax_status": "/fax-status/{fax_id}"
        }
    )
