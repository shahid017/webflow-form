from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pdf_generator import PDFGenerator
from fax_sender import FaxSender
from config import PHARMACY_FAX_NUMBER

app = FastAPI()

# Initialize services
pdf_generator = PDFGenerator()
fax_sender = FaxSender()

@app.post("/send-fax")
async def send_fax(request: Request):
    """
    Endpoint to receive form data, generate PDF, and send it as fax.
    """
    try:
        data = await request.json()
        
        # Step 1: Generate PDF from form data
        pdf_path = pdf_generator.generate_pdf(data, save_permanently=False)
        
        # Step 2: Send PDF as fax
        fax_result = fax_sender.send_pdf_as_fax(
            pdf_path=pdf_path,
            fax_number=PHARMACY_FAX_NUMBER,
            filename="refill_order.pdf"
        )
        
        # Step 3: Clean up temporary file
        fax_sender.cleanup_temp_file(pdf_path)
        
        if fax_result["success"]:
            return JSONResponse(content={
                "status": "success",
                "message": "PDF generated and fax sent successfully",
                "fax_id": fax_result.get("fax_id"),
                "fax_number": fax_result["fax_number"],
                "response_data": fax_result["response_data"]
            })
        else:
            return JSONResponse(content={
                "status": "error",
                "message": "PDF generated but fax failed",
                "error": fax_result["error"]
            }, status_code=500)

    except Exception as e:
        return JSONResponse(content={
            "status": "error", 
            "message": str(e)
        }, status_code=500)


@app.post("/generate-pdf")
async def generate_pdf_only(request: Request):
    """
    Endpoint to generate PDF from form data without sending fax.
    Useful for testing or when you only need the PDF.
    """
    try:
        data = await request.json()
        
        # Generate PDF and save permanently
        pdf_path = pdf_generator.generate_pdf(data, save_permanently=True)
        
        return JSONResponse(content={
            "status": "success",
            "message": "PDF generated successfully",
            "pdf_path": pdf_path
        })

    except Exception as e:
        return JSONResponse(content={
            "status": "error",
            "message": str(e)
        }, status_code=500)


@app.post("/send-fax-from-file")
async def send_fax_from_file(request: Request):
    """
    Endpoint to send an existing PDF file as fax.
    """
    try:
        data = await request.json()
        
        pdf_path = data.get("pdf_path")
        fax_number = data.get("fax_number", PHARMACY_FAX_NUMBER)
        filename = data.get("filename", "document.pdf")
        
        if not pdf_path:
            return JSONResponse(content={
                "status": "error",
                "message": "pdf_path is required"
            }, status_code=400)
        
        # Validate fax number
        if not fax_sender.validate_fax_number(fax_number):
            return JSONResponse(content={
                "status": "error",
                "message": "Invalid fax number format"
            }, status_code=400)
        
        # Send fax
        fax_result = fax_sender.send_pdf_as_fax(pdf_path, fax_number, filename)
        
        if fax_result["success"]:
            return JSONResponse(content={
                "status": "success",
                "message": "Fax sent successfully",
                "fax_id": fax_result.get("fax_id"),
                "fax_number": fax_result["fax_number"],
                "response_data": fax_result["response_data"]
            })
        else:
            return JSONResponse(content={
                "status": "error",
                "message": "Fax sending failed",
                "error": fax_result["error"]
            }, status_code=500)

    except Exception as e:
        return JSONResponse(content={
            "status": "error",
            "message": str(e)
        }, status_code=500)


@app.get("/fax-status/{fax_id}")
async def get_fax_status(fax_id: str):
    """
    Endpoint to check the status of a sent fax.
    """
    try:
        status_result = fax_sender.get_fax_status(fax_id)
        
        if status_result["success"]:
            return JSONResponse(content={
                "status": "success",
                "fax_id": fax_id,
                "fax_status": status_result["fax_status"]
            })
        else:
            return JSONResponse(content={
                "status": "error",
                "message": "Failed to get fax status",
                "error": status_result["error"]
            }, status_code=500)

    except Exception as e:
        return JSONResponse(content={
            "status": "error",
            "message": str(e)
        }, status_code=500)
