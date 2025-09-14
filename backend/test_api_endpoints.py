#!/usr/bin/env python3
import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✓ Root endpoint working")
            return True
        else:
            print(f"✗ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Root endpoint error: {e}")
        return False

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("✓ Health endpoint working")
            return True
        else:
            print(f"✗ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health endpoint error: {e}")
        return False

def test_registration():
    """Test user registration"""
    print("Testing user registration...")
    try:
        data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            "name": "Test User",
            "contact": "1234567890",
            "address": "Test Address"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        if response.status_code in [200, 201]:
            print("✓ User registration successful")
            return True
        else:
            print(f"✗ Registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Registration error: {e}")
        return False

def test_login():
    """Test user login"""
    print("Testing user login...")
    try:
        data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
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

def test_protected_endpoint(token):
    """Test protected endpoint with JWT token"""
    print("Testing protected endpoint...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            print("✓ Protected endpoint access successful")
            return True
        else:
            print(f"✗ Protected endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Protected endpoint error: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("=" * 50)
    print("API ENDPOINT TESTING")
    print("=" * 50)
    
    results = []
    
    results.append(test_root())
    results.append(test_health())
    results.append(test_registration())
    
    token = test_login()
    if token:
        results.append(True)
        results.append(test_protected_endpoint(token))
    else:
        results.append(False)
        results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Total tests: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("🎉 All API tests passed!")
        return True
    else:
        print("❌ Some tests failed.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)