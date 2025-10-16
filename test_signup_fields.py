#!/usr/bin/env python3
"""
Test script to verify the updated signup form field mappings
"""
import requests
import json

def test_signup_with_correct_fields():
    """Test the signup endpoint with the correct Webflow field names"""
    
    print("🧪 Testing signup endpoint with correct Webflow field names...")
    
    # Test data with actual Webflow field names
    signup_data = {
        "Form-first-name": "John",
        "Form-last-name": "Doe", 
        "Form-phone-number": "555-123-4567",
        "Form-date-of-brith": "1990-01-01",
        "address-input": "123 Main Street",
        "Form-area": "Downtown"
    }
    
    try:
        response = requests.post(
            "https://webflow-form.onrender.com/send-signup-fax",
            json=signup_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Signup endpoint working with correct field names!")
            result = response.json()
            print(f"Response: {result.get('message', 'No message')}")
            return True
        else:
            print(f"❌ Signup failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing signup: {e}")
        return False

def test_signup_minimal_fields():
    """Test with only required fields"""
    
    print("\n🧪 Testing signup with minimal required fields...")
    
    # Test data with only required fields
    signup_data = {
        "Form-first-name": "Jane",
        "Form-last-name": "Smith",
        "Form-phone-number": "555-987-6543"
    }
    
    try:
        response = requests.post(
            "https://webflow-form.onrender.com/send-signup-fax",
            json=signup_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Signup endpoint working with minimal fields!")
            return True
        else:
            print(f"❌ Signup failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing signup: {e}")
        return False

def test_signup_missing_required():
    """Test with missing required fields"""
    
    print("\n🧪 Testing signup with missing required fields...")
    
    # Test data missing required fields
    signup_data = {
        "Form-first-name": "John",
        # Missing last name and phone
        "Form-area": "Downtown"
    }
    
    try:
        response = requests.post(
            "https://webflow-form.onrender.com/send-signup-fax",
            json=signup_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 422:
            print("✅ Missing required fields properly returns 422!")
            print(f"Error message: {response.json().get('detail', 'No detail')}")
            return True
        else:
            print(f"❌ Should return 422 for missing fields, got: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing signup: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing updated signup form field mappings...\n")
    
    # Test with correct field names
    full_test_success = test_signup_with_correct_fields()
    
    # Test with minimal required fields
    minimal_test_success = test_signup_minimal_fields()
    
    # Test missing required fields
    missing_test_success = test_signup_missing_required()
    
    print(f"\n📊 Test Results:")
    print(f"Full field mapping: {'✅ PASS' if full_test_success else '❌ FAIL'}")
    print(f"Minimal fields: {'✅ PASS' if minimal_test_success else '❌ FAIL'}")
    print(f"Missing fields validation: {'✅ PASS' if missing_test_success else '❌ FAIL'}")
    
    # Summary
    all_success = full_test_success and minimal_test_success and missing_test_success
    if all_success:
        print("\n🎉 All signup field mapping tests passed!")
        print("\n📋 Updated field mappings:")
        print("✅ Form-first-name → first_name")
        print("✅ Form-last-name → last_name") 
        print("✅ Form-phone-number → phone")
        print("✅ Form-date-of-brith → date_of_birth")
        print("✅ address-input → address")
        print("✅ Form-area → area")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
