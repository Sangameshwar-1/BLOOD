import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000/api"

def test_connection():
    """Test basic server connection"""
    print("Testing server connection...")
    try:
        response = requests.get("http://127.0.0.1:5000/")
        if response.status_code == 200:
            print("✓ Server is running")
            return True
        else:
            print("✗ Server returned unexpected status code")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure it's running.")
        return False

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("\nTesting authentication endpoints...")
    
    # Test register
    register_data = {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "name": "Test User",
        "contact": "1234567890",
        "address": "Test Address"
    }
    
    try:
        # Register
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code in [200, 201]:
            print("✓ User registration successful")
        else:
            print(f"✗ Registration failed: {response.status_code} - {response.text}")
            return False
        
        # Login
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("token")
            print("✓ User login successful")
            
            # Test protected endpoint
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            if response.status_code == 200:
                print("✓ Protected endpoint access successful")
                return True
            else:
                print(f"✗ Protected endpoint failed: {response.status_code}")
                return False
        else:
            print(f"✗ Login failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Auth test failed: {e}")
        return False

def test_students_endpoints(token):
    """Test students endpoints with JWT token"""
    print("\nTesting students endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Create student
        student_data = {
            "name": "API Test Student",
            "age": 22,
            "branch": "Information Technology"
        }
        
        response = requests.post(f"{BASE_URL}/students/", json=student_data, headers=headers)
        if response.status_code == 201:
            student_id = response.json().get("student", {}).get("id")
            print("✓ Student created successfully")
            
            # Get all students
            response = requests.get(f"{BASE_URL}/students/", headers=headers)
            if response.status_code == 200:
                print("✓ Students retrieved successfully")
                
                # Get specific student
                response = requests.get(f"{BASE_URL}/students/{student_id}", headers=headers)
                if response.status_code == 200:
                    print("✓ Specific student retrieved successfully")
                    
                    # Clean up (delete student)
                    response = requests.delete(f"{BASE_URL}/students/{student_id}", headers=headers)
                    if response.status_code == 200:
                        print("✓ Student cleaned up successfully")
                        return True
                    else:
                        print(f"✗ Student cleanup failed: {response.status_code}")
                else:
                    print(f"✗ Get specific student failed: {response.status_code}")
            else:
                print(f"✗ Get students failed: {response.status_code}")
        else:
            print(f"✗ Create student failed: {response.status_code} - {response.text}")
            
        return False
        
    except Exception as e:
        print(f"✗ Students test failed: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("=" * 50)
    print("API TESTING SCRIPT")
    print("=" * 50)
    
    if not test_connection():
        return False
    
    if not test_auth_endpoints():
        return False
    
    # Get token for subsequent tests
    login_data = {"email": "testuser@example.com", "password": "testpassword123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = response.json().get("token")
    
    if not test_students_endpoints(token):
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All API tests passed!")
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)