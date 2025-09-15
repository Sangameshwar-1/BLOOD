#!/usr/bin/env python3
# simple_api_test.py
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_basic_endpoints():
    print("Testing basic endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✓ Root endpoint working")
        else:
            print(f"✗ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Root endpoint error: {e}")
        return False
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✓ Health endpoint working")
            return True
        else:
            print(f"✗ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health endpoint error: {e}")
        return False

def test_auth():
    print("\nTesting authentication...")
    
    # Register user
    try:
        data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            "name": "Test User",
            "contact": "1234567890",
            "address": "Test Address"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=data, timeout=5)
        if response.status_code in [200, 201]:
            print("✓ User registration successful")
        else:
            print(f"✗ Registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Registration error: {e}")
        return False
    
    # Login user
    try:
        data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=data, timeout=5)
        if response.status_code == 200:
            token = response.json().get("token")
            print("✓ User login successful")
            return token
        else:
            print(f"✗ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"✗ Login error: {e}")
        return None

def main():
    print("=" * 50)
    print("API TESTING")
    print("=" * 50)
    
    # Test basic endpoints
    if not test_basic_endpoints():
        print("❌ Basic endpoints test failed")
        return False
    
    # Test authentication
    token = test_auth()
    if not token:
        print("❌ Authentication test failed")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed!")
    print("Your Flask API is working correctly!")
    return True

if __name__ == "__main__":
    main()	
