#!/usr/bin/env python3
"""
Test script for PDF generation
"""
import json
from pdf_generator import generate_pdf

def test_pdf_generation():
    """Test PDF generation with sample data"""
    
    # Sample form data
    test_data = {
        "OR-Name": "John",
        "OR-Last-name": "Smith",
        "OR-Phone-number": "555-123-4567",
        "OR-Medication": "Aspirin, Ibuprofen, Vitamin D",
        "OR-note": "Please call when ready for pickup",
        "delivery_option": "Call when Ready",
        "address": "123 Main Street, Anytown, ST 12345",
        "time_slot": "2:00 PM - 4:00 PM"
    }
    
    print("🧪 Testing PDF generation with ReportLab...")
    print(f"📋 Test data: {json.dumps(test_data, indent=2)}")
    
    try:
        # Generate PDF using the new function
        pdf_path = generate_pdf(test_data, "test_prescription.pdf")
        
        print(f"✅ PDF generated successfully!")
        print(f"📄 PDF saved at: {pdf_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        return False

if __name__ == "__main__":
    test_pdf_generation()
