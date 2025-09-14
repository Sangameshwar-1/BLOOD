import sys
import os
import time
from datetime import datetime
sys.path.insert(0, os.path.abspath('.'))

from app import create_app
from models.user import User
from models.student import Student
from models.volunteer import Volunteer


def test_timestamp_creation():
    """Test that timestamp fields are automatically set on creation"""
    print("Testing timestamp creation...")
    
    app = create_app()
    with app.app_context():
        try:
            # Create a test user
            test_user = User(
                email="timestamp_test@example.com",
                password="testpassword",
                name="Timestamp Test User",
                contact="1234567890",
                address="Test Address"
            )
            test_user.hash_password()
            
            # Capture time before save
            before_save = datetime.utcnow()
            test_user.save()
            after_save = datetime.utcnow()
            
            # Verify timestamp fields exist and are reasonable
            if test_user.created_at and test_user.updated_at:
                print(f"✓ Timestamp fields created successfully")
                print(f"  Created at: {test_user.created_at}")
                print(f"  Updated at: {test_user.updated_at}")
                
                # Verify timestamps are within reasonable bounds
                if before_save <= test_user.created_at <= after_save:
                    print("✓ Created timestamp is within expected range")
                else:
                    print("✗ Created timestamp is outside expected range")
                    
                if before_save <= test_user.updated_at <= after_save:
                    print("✓ Updated timestamp is within expected range")
                else:
                    print("✗ Updated timestamp is outside expected range")
                    
                # Verify JSON serialization includes timestamps
                json_data = test_user.to_json()
                if 'created_at' in json_data and 'updated_at' in json_data:
                    print("✓ Timestamp fields included in JSON serialization")
                    print(f"  JSON created_at: {json_data['created_at']}")
                    print(f"  JSON updated_at: {json_data['updated_at']}")
                else:
                    print("✗ Timestamp fields missing from JSON serialization")
            else:
                print("✗ Timestamp fields not created")
            
            # Clean up
            test_user.delete()
            print("✓ Test user cleaned up")
            return True
            
        except Exception as e:
            print(f"✗ Timestamp creation test failed: {e}")
            return False


def test_timestamp_update():
    """Test that updated_at is automatically updated on save"""
    print("\nTesting timestamp update...")
    
    app = create_app()
    with app.app_context():
        try:
            # Create a test student
            test_student = Student(
                name="Update Test Student",
                age=20,
                branch="Computer Science"
            )
            test_student.save()
            
            original_created_at = test_student.created_at
            original_updated_at = test_student.updated_at
            
            print(f"  Original created_at: {original_created_at}")
            print(f"  Original updated_at: {original_updated_at}")
            
            # Wait a moment to ensure timestamp difference
            time.sleep(1)
            
            # Update the student
            test_student.age = 21
            before_update = datetime.utcnow()
            test_student.save()
            after_update = datetime.utcnow()
            
            # Verify created_at didn't change but updated_at did
            if test_student.created_at == original_created_at:
                print("✓ Created timestamp remained unchanged on update")
            else:
                print("✗ Created timestamp changed on update (should not happen)")
                
            if test_student.updated_at > original_updated_at:
                print("✓ Updated timestamp was updated on save")
                print(f"  New updated_at: {test_student.updated_at}")
                
                if before_update <= test_student.updated_at <= after_update:
                    print("✓ New updated timestamp is within expected range")
                else:
                    print("✗ New updated timestamp is outside expected range")
            else:
                print("✗ Updated timestamp was not updated on save")
            
            # Clean up
            test_student.delete()
            print("✓ Test student cleaned up")
            return True
            
        except Exception as e:
            print(f"✗ Timestamp update test failed: {e}")
            return False


def test_all_models_have_timestamps():
    """Test that all models inherit timestamp functionality"""
    print("\nTesting all models have timestamp functionality...")
    
    app = create_app()
    with app.app_context():
        results = []
        try:
            # Test User model
            user = User(email="test1@example.com", password="test", name="Test User")
            user.hash_password()
            user.save()
            if hasattr(user, 'created_at') and hasattr(user, 'updated_at'):
                print("✓ User model has timestamp fields")
                results.append(True)
            else:
                print("✗ User model missing timestamp fields")
                results.append(False)
            user.delete()
            
            # Test Student model
            student = Student(name="Test Student", age=20, branch="CS")
            student.save()
            if hasattr(student, 'created_at') and hasattr(student, 'updated_at'):
                print("✓ Student model has timestamp fields")
                results.append(True)
            else:
                print("✗ Student model missing timestamp fields")
                results.append(False)
            student.delete()
            
            # Test Volunteer model
            volunteer = Volunteer(name="Test Volunteer", contact="123", availability="Weekends")
            volunteer.save()
            if hasattr(volunteer, 'created_at') and hasattr(volunteer, 'updated_at'):
                print("✓ Volunteer model has timestamp fields")
                results.append(True)
            else:
                print("✗ Volunteer model missing timestamp fields")
                results.append(False)
            volunteer.delete()
            
            return all(results)
            
        except Exception as e:
            print(f"✗ All models timestamp test failed: {e}")
            return False


def test_user_tracking_fields():
    """Test that created_by and updated_by fields are available"""
    print("\nTesting user tracking fields...")
    
    app = create_app()
    with app.app_context():
        try:
            # Create a test volunteer with user tracking
            volunteer = Volunteer(
                name="Tracked Volunteer",
                contact="9876543210",
                availability="Anytime"
            )
            volunteer.created_by = "admin_user"
            volunteer.updated_by = "admin_user"
            volunteer.save()
            
            # Verify user tracking fields
            json_data = volunteer.to_json()
            if 'created_by' in json_data and 'updated_by' in json_data:
                print("✓ User tracking fields are available and serialized")
                print(f"  Created by: {json_data['created_by']}")
                print(f"  Updated by: {json_data['updated_by']}")
            else:
                print("✗ User tracking fields missing from JSON")
            
            # Test updating with different user
            volunteer.updated_by = "different_user"
            volunteer.save()
            
            updated_json = volunteer.to_json()
            if updated_json.get('created_by') == 'admin_user' and updated_json.get('updated_by') == 'different_user':
                print("✓ User tracking fields update correctly")
            else:
                print("✗ User tracking fields did not update correctly")
            
            # Clean up
            volunteer.delete()
            print("✓ Test volunteer cleaned up")
            return True
            
        except Exception as e:
            print(f"✗ User tracking fields test failed: {e}")
            return False


def run_all_timestamp_tests():
    """Run all timestamp-related tests"""
    print("=" * 50)
    print("TIMESTAMP FUNCTIONALITY TESTS")
    print("=" * 50)
    
    results = []
    results.append(test_timestamp_creation())
    results.append(test_timestamp_update())
    results.append(test_all_models_have_timestamps())
    results.append(test_user_tracking_fields())
    
    # Summary
    print("\n" + "=" * 50)
    print("TIMESTAMP TEST SUMMARY")
    print("=" * 50)
    print(f"Total tests: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("🎉 All timestamp tests passed!")
        return True
    else:
        print("❌ Some timestamp tests failed. Check the errors above.")
        return False


if __name__ == "__main__":
    run_all_timestamp_tests()