#!/usr/bin/env python3
"""
Test script to generate sample PDFs and compare formats
"""
import os
from pdf_generator import generate_pdf, generate_signup_pdf

def test_prescription_pdf():
    """Generate a sample prescription PDF"""
    print("🧪 Generating sample prescription PDF...")
    
    prescription_data = {
        "OR-Name": "John",
        "OR-Last-name": "Doe", 
        "OR-Phone-number": "555-123-4567",
        "OR-Medication": "Aspirin, Ibuprofen, Vitamin D",
        "OR-note": "Please call when ready for pickup",
        "delivery_option": "Call when Ready",
        "address": "123 Main Street, Anytown, ST 12345",
        "time_slot": "2:00 PM - 4:00 PM"
    }
    
    output_file = "test_prescription_current.pdf"
    result = generate_pdf(prescription_data, output_file)
    
    if result:
        print(f"✅ Prescription PDF generated: {os.path.abspath(result)}")
        return True
    else:
        print("❌ Failed to generate prescription PDF")
        return False

def test_signup_pdf():
    """Generate a sample signup PDF"""
    print("🧪 Generating sample signup PDF...")
    
    signup_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com", 
        "phone": "555-987-6543",
        "date_of_birth": "1990-01-15",
        "address": "456 Oak Avenue",
        "city": "Springfield",
        "state": "NY",
        "postal_code": "12345",
        "emergency_contact": "Bob Smith",
        "emergency_phone": "555-111-2222",
        "notes": "Prefers morning appointments"
    }
    
    output_file = "test_signup_current.pdf"
    result = generate_signup_pdf(signup_data, output_file)
    
    if result:
        print(f"✅ Signup PDF generated: {os.path.abspath(result)}")
        return True
    else:
        print("❌ Failed to generate signup PDF")
        return False

if __name__ == "__main__":
    print("🚀 Generating sample PDFs for format comparison...\n")
    
    prescription_success = test_prescription_pdf()
    signup_success = test_signup_pdf()
    
    print(f"\n📊 Results:")
    print(f"Prescription PDF: {'✅ Generated' if prescription_success else '❌ Failed'}")
    print(f"Signup PDF: {'✅ Generated' if signup_success else '❌ Failed'}")
    
    if prescription_success and signup_success:
        print("\n📁 Check the generated PDF files to see current format")
        print("   - test_prescription_current.pdf")
        print("   - test_signup_current.pdf")
