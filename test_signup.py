#!/usr/bin/env python3
"""
Test script for the signup form endpoint
"""
import requests
import json

def test_signup_endpoint():
    """Test the signup form endpoint"""
    
    # Test data
    signup_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "555-123-4567",
        "date_of_birth": "1990-01-15",
        "address": "123 Main Street",
        "city": "Anytown",
        "state": "CA",
        "postal_code": "12345",
        "emergency_contact": "Jane Doe",
        "emergency_phone": "555-987-6543",
        "notes": "Prefers morning appointments"
    }
    
    # Test with JSON data
    print("🧪 Testing signup endpoint with JSON data...")
    try:
        response = requests.post(
            "https://webflow-form.onrender.com/send-signup-fax",
            json=signup_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Signup endpoint test successful!")
            return True
        else:
            print("❌ Signup endpoint test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing signup endpoint: {e}")
        return False

def test_signup_form_data():
    """Test with form-encoded data (like Webflow would send)"""
    
    # Test data as form fields
    form_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone": "555-987-6543",
        "date_of_birth": "1985-05-20",
        "address": "456 Oak Avenue",
        "city": "Springfield",
        "state": "NY",
        "postal_code": "54321",
        "emergency_contact": "Bob Smith",
        "emergency_phone": "555-111-2222",
        "notes": "Allergic to penicillin"
    }
    
    print("\n🧪 Testing signup endpoint with form data...")
    try:
        response = requests.post(
            "https://webflow-form.onrender.com/send-signup-fax",
            data=form_data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Signup form data test successful!")
            return True
        else:
            print("❌ Signup form data test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing signup form data: {e}")
        return False

def test_debug_endpoint():
    """Test the debug endpoint to see what data is received"""
    
    test_data = {
        "firstName": "Test",
        "lastName": "User",
        "emailAddress": "test@example.com",
        "phoneNumber": "555-000-0000"
    }
    
    print("\n🧪 Testing debug endpoint...")
    try:
        response = requests.post(
            "https://webflow-form.onrender.com/debug-form-data",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Debug endpoint test successful!")
            return True
        else:
            print("❌ Debug endpoint test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing debug endpoint: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting signup form tests...\n")
    
    # Test debug endpoint first
    debug_success = test_debug_endpoint()
    
    # Test signup endpoint with JSON
    json_success = test_signup_endpoint()
    
    # Test signup endpoint with form data
    form_success = test_signup_form_data()
    
    print(f"\n📊 Test Results:")
    print(f"Debug Endpoint: {'✅ PASS' if debug_success else '❌ FAIL'}")
    print(f"JSON Signup: {'✅ PASS' if json_success else '❌ FAIL'}")
    print(f"Form Signup: {'✅ PASS' if form_success else '❌ FAIL'}")
    
    if all([debug_success, json_success, form_success]):
        print("\n🎉 All tests passed! Signup form is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
