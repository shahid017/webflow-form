# Load environment variables from .env file FIRST
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from pdf_generator import generate_pdf, generate_signup_pdf
from fax_sender import FaxSender
from config import PHARMACY_FAX_NUMBER
from models import FormData, SignupData, SendFaxFromFileRequest, ApiResponse, HealthResponse

app = FastAPI(
    title="Webflow Form to Fax API",
    description="API to receive form data from Webflow and send it as fax via Sinch",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for Webflow integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://westmount-pharmacy.webflow.io",  # Your Webflow domain
        "http://localhost:3000",  # For local development
        "http://localhost:8080",  # Alternative local port
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
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

@app.post("/send-signup-fax", response_model=ApiResponse)
async def send_signup_fax(request: Request):
    """
    Endpoint to receive signup form data, generate PDF, and send it as fax.
    
    This endpoint accepts signup form data from Webflow, generates a PDF document,
    and sends it as a fax using the Sinch API.
    """
    try:
        # Get content type to determine how to parse the data
        content_type = request.headers.get("content-type", "")
        
        # Parse data based on content type
        raw_data = {}
        if "application/json" in content_type:
            try:
                raw_data = await request.json()
                print(f"Received JSON signup data: {raw_data}")
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                raw_data = {}
        else:
            # Handle form-encoded data (application/x-www-form-urlencoded)
            try:
                form_data = await request.form()
                raw_data = dict(form_data)
                print(f"Received form signup data: {raw_data}")
            except Exception as e:
                print(f"Error parsing form data: {e}")
                raw_data = {}
        
        # Log the incoming data for debugging
        print(f"Content-Type: {content_type}")
        print(f"Parsed signup data: {raw_data}")
        print(f"Raw form data keys: {list(raw_data.keys()) if raw_data else 'No data'}")
        
        # Check if we have any data
        if not raw_data:
            raise HTTPException(
                status_code=400, 
                detail="No form data received. Please ensure you're sending the required signup form fields."
            )
        
        # Map common Webflow field variations to our expected format
        data = {}
        
        # Map field names (handle various formats Webflow might send)
        field_mappings = {
            'first_name': ['Form-first-name', 'Form first name', 'first_name', 'firstName', 'fname', 'first-name'],
            'last_name': ['Form-last-name', 'Form last name', 'last_name', 'lastName', 'lname', 'last-name', 'surname'],
            'phone': ['Form-phone-number', 'Form phone number', 'phone', 'phone_number', 'phoneNumber', 'telephone', 'mobile'],
            'date_of_birth': ['Form-date-of-brith', 'Form Phone Number 2', 'date_of_birth', 'dateOfBirth', 'dob', 'birth_date', 'birthdate'],
            'address': ['address-input', 'Form transfer', 'address', 'street_address', 'streetAddress', 'street'],
            'area': ['Form-area', 'Form area', 'area', 'city', 'town', 'region'],
            'email': ['email', 'email_address', 'emailAddress', 'e-mail'],  # Keep as optional
            'emergency_contact': ['emergency_contact', 'emergencyContact', 'emergency_name'],  # Keep as optional
            'emergency_phone': ['emergency_phone', 'emergencyPhone', 'emergency_number'],  # Keep as optional
            'notes': ['notes', 'comments', 'additional_info', 'special_instructions']  # Keep as optional
        }
        
        # Try to map each expected field
        for expected_field, possible_names in field_mappings.items():
            for name in possible_names:
                if name in raw_data:
                    data[expected_field] = raw_data[name]
                    break
        
        # Validate required fields (based on actual Webflow form)
        required_fields = ['first_name', 'last_name', 'phone']
        missing_fields = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            raise HTTPException(
                status_code=422, 
                detail=f"Missing required fields: {', '.join(missing_fields)}. Received data: {raw_data}"
            )
        
        print(f"Mapped signup form data: {data}")
        
        # Step 1: Generate PDF from signup form data
        import uuid
        pdf_id = str(uuid.uuid4())[:8]  # Short unique ID
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            pdf_path = generate_signup_pdf(data, temp_file.name)
        
        # Store PDF for serving
        temp_pdfs[pdf_id] = pdf_path
        
        # Step 2: Create public URL for the PDF
        base_url = "https://webflow-form.onrender.com"  # Your Render URL
        pdf_url = f"{base_url}/pdf/{pdf_id}"
        
        # Step 3: Send PDF as fax using the public URL
        fax_result = fax_sender.send_pdf_with_url(
            pdf_url=pdf_url,
            fax_number=PHARMACY_FAX_NUMBER,  # You can change this to a different fax number for signups
            filename="patient_registration.pdf"
        )
        
        # Step 4: Clean up temporary file after some delay
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
                message="Signup PDF generated and fax sent successfully",
                fax_id=fax_result.get("fax_id"),
                fax_number=fax_result["fax_number"],
                response_data=fax_result["response_data"]
            )
        else:
            return ApiResponse(
                status="error",
                message="Signup PDF generated but fax failed",
                error=fax_result["error"]
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Alternative endpoint with underscores for compatibility
@app.post("/send_signup_fax", response_model=ApiResponse)
async def send_signup_fax_alt(request: Request):
    """
    Alternative endpoint for signup form data with underscore format.
    This redirects to the main signup endpoint for compatibility.
    """
    return await send_signup_fax(request)

@app.post("/send-fax", response_model=ApiResponse)
async def send_fax(request: Request):
    """
    Endpoint to receive form data, generate PDF, and send it as fax.
    
    This endpoint accepts form data from Webflow, generates a PDF document,
    and sends it as a fax using the Sinch API.
    """
    try:
        # Get content type to determine how to parse the data
        content_type = request.headers.get("content-type", "")
        
        # Parse data based on content type
        raw_data = {}
        if "application/json" in content_type:
            try:
                raw_data = await request.json()
                print(f"Received JSON data: {raw_data}")
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                raw_data = {}
        else:
            # Handle form-encoded data (application/x-www-form-urlencoded)
            try:
                form_data = await request.form()
                raw_data = dict(form_data)
                print(f"Received form data: {raw_data}")
            except Exception as e:
                print(f"Error parsing form data: {e}")
                raw_data = {}
        
        # Log the incoming data for debugging
        print(f"Content-Type: {content_type}")
        print(f"Parsed data: {raw_data}")
        print(f"Raw data keys: {list(raw_data.keys()) if raw_data else 'No data'}")
        
        # Check if we have any data
        if not raw_data:
            raise HTTPException(
                status_code=400, 
                detail="No form data received. Please ensure you're sending the required form fields."
            )
        
        # Map common Webflow field variations to our expected format
        data = {}
        
        # Map field names (handle various formats Webflow might send)
        field_mappings = {
            'OR-Name': ['OR-Name', 'OR_Name', 'first_name', 'firstName', 'name'],
            'OR-Last-name': ['OR-Last-name', 'OR_Last_name', 'last_name', 'lastName', 'surname'],
            'OR-Phone-number': ['OR-Phone-number', 'OR_Phone_number', 'phone_number', 'phoneNumber', 'phone', 'telephone'],
            'OR-Medication': ['OR-Medication', 'OR_Medication', 'medication', 'medications', 'drugs'],
            'OR-note': ['OR-note', 'OR_note', 'note', 'notes', 'special_instructions', 'comments'],
            'delivery_option': ['OR-Delivery-or-Pick-up', 'delivery_option', 'deliveryOption', 'delivery', 'pickup_option'],
            'address': ['Form-transfer', 'address', 'delivery_address', 'deliveryAddress', 'street_address'],
            'time_slot': ['OR-Tomorrow-delivery-time', 'time_slot', 'timeSlot', 'preferred_time', 'time_preference']
        }
        
        # Try to map each expected field
        for expected_field, possible_names in field_mappings.items():
            for name in possible_names:
                if name in raw_data:
                    data[expected_field] = raw_data[name]
                    break
        
        # Validate required fields
        required_fields = ['OR-Name', 'OR-Last-name', 'OR-Phone-number', 'OR-Medication']
        missing_fields = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            raise HTTPException(
                status_code=422, 
                detail=f"Missing required fields: {', '.join(missing_fields)}. Received data: {raw_data}"
            )
        
        print(f"Mapped form data: {data}")
        
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


@app.post("/debug-form-data")
async def debug_form_data(request: Request):
    """
    Debug endpoint to see exactly what data Webflow is sending.
    Use this to troubleshoot form field mapping issues.
    """
    try:
        # Get content type to determine how to parse the data
        content_type = request.headers.get("content-type", "")
        
        # Parse data based on content type
        if "application/json" in content_type:
            raw_data = await request.json()
            data_source = "JSON"
        else:
            # Handle form-encoded data (application/x-www-form-urlencoded)
            form_data = await request.form()
            raw_data = dict(form_data)
            data_source = "Form Data"
        
        return {
            "status": "debug",
            "message": "Form data received successfully",
            "content_type": content_type,
            "data_source": data_source,
            "received_data": raw_data,
            "field_names": list(raw_data.keys()) if isinstance(raw_data, dict) else "Not a dictionary",
            "data_types": {k: type(v).__name__ for k, v in raw_data.items()} if isinstance(raw_data, dict) else "Not a dictionary"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing request: {str(e)}",
            "content_type": request.headers.get("content-type", "unknown")
        }

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
            "send_signup_fax": "/send-signup-fax",
            "send_signup_fax_alt": "/send_signup_fax",
            "generate_pdf": "/generate-pdf",
            "send_fax_from_file": "/send-fax-from-file",
            "fax_status": "/fax-status/{fax_id}",
            "debug_form_data": "/debug-form-data"
        }
    )
