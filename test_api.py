#!/usr/bin/env python3
"""
Test script for the Webflow form to fax API
"""
import requests
import json
import time

# Test data - simulating Webflow form submission
test_data = {
    "OR-Name": "John",
    "OR-Last-name": "Doe", 
    "OR-Phone-number": "123-456-7890",
    "OR-Medication": "Aspirin, Ibuprofen, Vitamin D",
    "OR-note": "Please call when ready for pickup",
    "delivery_option": "Delivery",
    "address": "123 Main Street, City, State 12345",
    "time_slot": "2:00 PM - 4:00 PM"
}

def test_pdf_generation():
    """Test PDF generation endpoint"""
    print("🧪 Testing PDF Generation...")
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-pdf",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ PDF Generation Successful!")
            print(f"📄 PDF Path: {result.get('pdf_path')}")
            return True
        else:
            print(f"❌ PDF Generation Failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_send_fax():
    """Test complete send fax workflow"""
    print("\n🧪 Testing Send Fax Workflow...")
    
    try:
        response = requests.post(
            "http://localhost:8000/send-fax",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Send Fax Successful!")
            print(f"📧 Fax ID: {result.get('fax_id')}")
            print(f"📞 Fax Number: {result.get('fax_number')}")
            return result.get('fax_id')
        else:
            print(f"❌ Send Fax Failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def test_fax_status(fax_id):
    """Test fax status endpoint"""
    if not fax_id:
        return
        
    print(f"\n🧪 Testing Fax Status for ID: {fax_id}...")
    
    try:
        response = requests.get(f"http://localhost:8000/fax-status/{fax_id}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Fax Status Retrieved!")
            print(f"📊 Status: {result.get('fax_status')}")
        else:
            print(f"❌ Fax Status Failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    print("🚀 Starting API Tests...")
    print("=" * 50)
    
    # Test 1: PDF Generation only
    pdf_success = test_pdf_generation()
    
    # Test 2: Complete workflow (only if PDF generation works)
    if pdf_success:
        fax_id = test_send_fax()
        
        # Test 3: Fax Status (only if fax was sent)
        if fax_id:
            time.sleep(2)  # Wait a bit before checking status
            test_fax_status(fax_id)
    
    print("\n" + "=" * 50)
    print("🏁 Testing Complete!")

if __name__ == "__main__":
    main()
