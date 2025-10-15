"""
Pydantic models for the Webflow form to fax API
"""
from pydantic import BaseModel, Field
from typing import Optional


class FormData(BaseModel):
    """Model for Webflow form submission data"""
    
    # Required fields
    OR_Name: str = Field(..., description="Patient's first name", example="John", alias="OR-Name")
    OR_Last_name: str = Field(..., description="Patient's last name", example="Smith", alias="OR-Last-name")
    OR_Phone_number: str = Field(..., description="Patient's phone number", example="555-123-4567", alias="OR-Phone-number")
    OR_Medication: str = Field(..., description="Medications (comma-separated)", example="Aspirin, Ibuprofen, Vitamin D", alias="OR-Medication")
    
    # Optional fields
    OR_note: Optional[str] = Field(None, description="Special notes or instructions", example="Please call when ready", alias="OR-note")
    delivery_option: Optional[str] = Field(None, description="Delivery option", example="Call when Ready")
    address: Optional[str] = Field(None, description="Delivery address", example="123 Main St, City, State 12345")
    time_slot: Optional[str] = Field(None, description="Preferred time slot", example="2:00 PM - 4:00 PM")
    
    class Config:
        allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "OR-Name": "John",
                "OR-Last-name": "Smith",
                "OR-Phone-number": "555-123-4567",
                "OR-Medication": "Aspirin, Ibuprofen, Vitamin D",
                "OR-note": "Please call when ready for pickup",
                "delivery_option": "Call when Ready",
                "address": "123 Main Street, Anytown, ST 12345",
                "time_slot": "2:00 PM - 4:00 PM"
            }
        }


class SendFaxFromFileRequest(BaseModel):
    """Model for sending fax from existing PDF file"""
    
    pdf_path: str = Field(..., description="Path to the PDF file", example="/path/to/document.pdf")
    fax_number: Optional[str] = Field(None, description="Destination fax number", example="17057415595")
    filename: Optional[str] = Field("document.pdf", description="Name for the fax file", example="refill_order.pdf")
    
    class Config:
        json_schema_extra = {
            "example": {
                "pdf_path": "/path/to/document.pdf",
                "fax_number": "17057415595",
                "filename": "refill_order.pdf"
            }
        }


class ApiResponse(BaseModel):
    """Standard API response model"""
    
    status: str = Field(..., description="Response status", example="success")
    message: str = Field(..., description="Response message", example="PDF generated and fax sent successfully")
    fax_id: Optional[str] = Field(None, description="Fax ID from Sinch", example="fax_abc123")
    fax_number: Optional[str] = Field(None, description="Destination fax number", example="17057415595")
    pdf_path: Optional[str] = Field(None, description="Path to generated PDF", example="/path/to/document.pdf")
    response_data: Optional[dict] = Field(None, description="Additional response data from Sinch")
    error: Optional[str] = Field(None, description="Error message if status is error")


class HealthResponse(BaseModel):
    """Health check response model"""
    
    status: str = Field(..., description="API status", example="healthy")
    message: str = Field(..., description="Status message", example="Webflow Form to Fax API is running")
    version: str = Field(..., description="API version", example="1.0.0")
    endpoints: dict = Field(..., description="Available endpoints")
