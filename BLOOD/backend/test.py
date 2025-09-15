#!/usr/bin/env python3
try:
    import requests
except ImportError:
    import sys
    print("The 'requests' module is not installed. Please install it using 'pip install requests'.")
    sys.exit(1)

import sys
import time

BASE_URL = "http://localhost:5000/api"

class APITester:
    def __init__(self):
        self.token = None
        self.user_id = None
        self.student_id = None
        self.donor_id = None
        self.volunteer_id = None

    def print_section(self, title):
        print(f"\n{'='*60}")
        print(f"{title.upper()}")
        print(f"{'='*60}")

    def test_connection(self):
        """Test basic server connection"""
        print("Testing server connection...")
        try:
            response = requests.get("http://localhost:5000/", timeout=5)
            if response.status_code == 200:
                print("✓ Server is running")
                return True
            else:
                print(f"✗ Server returned status: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("✗ Cannot connect to server")
            return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False

    def test_auth(self):
        """Test authentication endpoints"""
        self.print_section("Authentication Tests")
        
        # Test registration
        print("1. Testing user registration...")
        register_data = {
            "email": "testuser3@example.com",
            "password": "testpassword123",
            "name": "Test User",
            "contact": "1234567890",
            "address": "Test Address"
        }

        try:
            response = requests.post(f"{BASE_URL}/auth/register", json=register_data, timeout=5)
            if response.status_code in [200, 201]:
                print("✓ User registration successful")
                print(f"User ID: {response.json().get('user', {}).get('id')}")
            elif response.status_code == 409:  # Handle "User already exists"
                print("✓ User already exists, proceeding with login")
            else:
                print(f"✗ Registration failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ Registration error: {e}")
            return False


        # Test login
        print("\n2. Testing user login...")
        login_data = {
            "email": "testuser3@example.com",
            "password": "testpassword123"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=5)
            if response.status_code == 200:
                self.token = response.json().get("token")
                print("✓ User login successful")
                print(f"User ID: {response.json().get('user', {}).get('id')}\n")
                print(f"   Token: {self.token}")
                return True
            else:
                print(f"✗ Login failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ Login error: {e}")
            return False

    def test_students(self):
        """Test student endpoints"""
        self.print_section("Student Management Tests")
        
        if not self.token:
            print("✗ No authentication token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        
        # Test create student
        print("1. Testing student creation...")
        student_data = {
            "creator_id": self.user_id,
            "name": "John Doe",
            "age": 22,
            "branch": "Computer Science"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/students/", json=student_data, headers=headers, timeout=5)
            if response.status_code == 201:
                self.student_id = response.json().get("student", {}).get("id")
                print("✓ Student created successfully")
                print(f"   Student ID: {self.student_id}")
            else:
                print(f"✗ Student creation failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ Student creation error: {e}")
            return False

        # Test get all students
        print("\n2. Testing get all students...")
        try:
            response = requests.get(f"{BASE_URL}/students/", headers=headers, timeout=5)
            if response.status_code == 200:
                students = response.json()
                print(f"✓ Retrieved {len(students)} students")
            else:
                print(f"✗ Get students failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Get students error: {e}")
            return False

        # Test get specific student
        print("\n3. Testing get specific student...")
        try:
            response = requests.get(f"{BASE_URL}/students/{self.student_id}", headers=headers, timeout=5)
            if response.status_code == 200:
                student = response.json()
                print(f"✓ Student retrieved: {student.get('name')}")
            else:
                print(f"✗ Get student failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Get student error: {e}")
            return False

        # Test update student
        print("\n4. Testing student update...")
        update_data = {"age": 23}
        try:
            response = requests.put(f"{BASE_URL}/students/{self.student_id}", json=update_data, headers=headers, timeout=5)
            if response.status_code == 200:
                print("✓ Student updated successfully")
            else:
                print(f"✗ Student update failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Student update error: {e}")
            return False

        # Test delete student
        print("\n5. Testing student deletion...")
        try:
            response = requests.delete(f"{BASE_URL}/students/{self.student_id}", headers=headers, timeout=5)
            if response.status_code == 200:
                print("✓ Student deleted successfully")
            else:
                print(f"✗ Student deletion failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Student deletion error: {e}")
            return False

        return True

    def test_donors(self):
        """Test donor endpoints"""
        self.print_section("Donor Management Tests")
        
        if not self.token:
            print("✗ No authentication token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        
        # Test create donor
        print("1. Testing donor creation...")
        donor_data = {
            "creator_id": self.user_id,
            "name": "Jane Smith",
            "blood_type": "O+",
            "contact": "9876543210",
            "address": "123 Donor Street",
            "district": "Central District",
            "weight": 65.5
        }
        
        try:
            response = requests.post(f"{BASE_URL}/donors/", json=donor_data, headers=headers, timeout=5)
            if response.status_code == 201:
                self.donor_id = response.json().get("donor", {}).get("id")
                print("✓ Donor created successfully")
                print(f"   Donor ID: {self.donor_id}")
            else:
                print(f"✗ Donor creation failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ Donor creation error: {e}")
            return False

        # Test get all donors
        print("\n2. Testing get all donors...")
        try:
            response = requests.get(f"{BASE_URL}/donors/", headers=headers, timeout=5)
            if response.status_code == 200:
                donors = response.json()
                print(f"✓ Retrieved {len(donors)} donors")
            else:
                print(f"✗ Get donors failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Get donors error: {e}")
            return False

        # Test delete donor
        print("\n3. Testing donor deletion...")
        try:
            response = requests.delete(f"{BASE_URL}/donors/{self.donor_id}", headers=headers, timeout=5)
            if response.status_code == 200:
                print("✓ Donor deleted successfully")
                return True
            else:
                print(f"✗ Donor deletion failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Donor deletion error: {e}")
            return False
    def test_volunteers(self):
        """Test volunteer endpoints"""
        self.print_section("Volunteer Management Tests")
        
        if not self.token:
            print("✗ No authentication token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        
        # Test create volunteer
        print("1. Testing volunteer creation...")
        volunteer_data = {
            "creator_id": self.user_id,
            "name": "Alice Johnson",
            "contact": "5551234567",
            "address": "456 Volunteer Ave",
            "district": "North District"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/volunteers/", json=volunteer_data, headers=headers, timeout=5)
            if response.status_code == 201:
                self.volunteer_id = response.json().get("volunteer", {}).get("id")
                print("✓ Volunteer created successfully")
                print(f"   Volunteer ID: {self.volunteer_id}")
            else:
                print(f"✗ Volunteer creation failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ Volunteer creation error: {e}")
            return False

        # Test get all volunteers
        print("\n2. Testing get all volunteers...")
        try:
            response = requests.get(f"{BASE_URL}/volunteers/", headers=headers, timeout=5)
            if response.status_code == 200:
                volunteers = response.json()
                print(f"✓ Retrieved {len(volunteers)} volunteers")
            else:
                print(f"✗ Get volunteers failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Get volunteers error: {e}")
            return False

        # Test delete volunteer
        print("\n3. Testing volunteer deletion...")
        try:
            response = requests.delete(f"{BASE_URL}/volunteers/{self.volunteer_id}", headers=headers, timeout=5)
            if response.status_code == 200:
                print("✓ Volunteer deleted successfully")
            else:
                print(f"✗ Volunteer deletion failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Volunteer deletion error: {e}")
            return False

        return True
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("COMPREHENSIVE API TESTING")
        print("=" * 60)
        
        time.sleep(2)
        
        results = []
        
        # Test server connection
        results.append(self.test_connection() or False)
        if not all(results):
            print("❌ Cannot proceed without server connection")
            return False
        
        # Test authentication
        results.append(self.test_auth() or False)
        if not all(results):
            print("❌ Cannot proceed without authentication")
            return False
        
        # Test students
        results.append(self.test_students() or False)
        
        # Test donors
        results.append(self.test_donors() or False)
        
        # Test volunteers
        results.append(self.test_volunteers() or False)
        
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total test groups: {len(results)}")
        print(f"Passed: {sum(results)}")
        print(f"Failed: {len(results) - sum(results)}")
        
        if all(results):
            print("\n🎉 All tests passed!")
            return True
        else:
            print("\n❌ Some tests failed. Check the logs above.")
            return False
if __name__ == "__main__":
    tester = APITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)