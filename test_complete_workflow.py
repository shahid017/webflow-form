#!/usr/bin/env python3
"""
Test the complete workflow: PDF generation + Upload + Fax sending
"""
import json
from pdf_generator import generate_pdf
from fax_sender import FaxSender
from config import PHARMACY_FAX_NUMBER

def test_complete_workflow():
    """Test the complete workflow from form data to fax"""
    
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
    
    print("🧪 Testing Complete Workflow...")
    print("=" * 50)
    print(f"📋 Test data: {json.dumps(test_data, indent=2)}")
    print("=" * 50)
    
    try:
        # Step 1: Generate PDF
        print("\n📄 Step 1: Generating PDF...")
        pdf_path = generate_pdf(test_data, "test_prescription_workflow.pdf")
        print(f"✅ PDF generated: {pdf_path}")
        
        # Step 2: Send Fax
        print("\n📤 Step 2: Sending Fax...")
        fax_sender = FaxSender()
        result = fax_sender.send_pdf_as_fax(pdf_path, PHARMACY_FAX_NUMBER, "prescription_refill.pdf")
        
        if result["success"]:
            print("✅ Fax sent successfully!")
            print(f"📋 Fax ID: {result['fax_id']}")
            print(f"📞 Fax Number: {result['fax_number']}")
            print(f"🔗 Content URL: {result['content_url']}")
        else:
            print("❌ Fax sending failed!")
            print(f"Error: {result['error']}")
        
        return result["success"]
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_workflow()
    print(f"\n{'🎉 SUCCESS!' if success else '❌ FAILED!'}")
