#!/usr/bin/env python
"""
Simple test to validate timestamp field structure and functionality
without requiring a MongoDB connection.
"""
import sys
import os
from datetime import datetime, timezone
sys.path.insert(0, os.path.abspath('.'))

from models.base import TimestampedDocument
from models.user import User
from models.student import Student
from models.volunteer import Volunteer
from models.donor import Donor


def test_model_inheritance():
    """Test that all models properly inherit from TimestampedDocument"""
    print("Testing model inheritance...")
    
    models = [
        ('User', User),
        ('Student', Student),
        ('Volunteer', Volunteer),
        ('Donor', Donor)
    ]
    
    for model_name, model_class in models:
        if issubclass(model_class, TimestampedDocument):
            print(f"✓ {model_name} inherits from TimestampedDocument")
        else:
            print(f"✗ {model_name} does not inherit from TimestampedDocument")
            return False
    
    return True


def test_timestamp_fields():
    """Test that all models have timestamp fields"""
    print("\nTesting timestamp fields presence...")
    
    models = [
        ('User', User),
        ('Student', Student),
        ('Volunteer', Volunteer),
        ('Donor', Donor)
    ]
    
    for model_name, model_class in models:
        instance = model_class()
        
        # Check for timestamp fields
        has_created_at = hasattr(instance, 'created_at')
        has_updated_at = hasattr(instance, 'updated_at')
        has_created_by = hasattr(instance, 'created_by')
        has_updated_by = hasattr(instance, 'updated_by')
        
        if has_created_at and has_updated_at and has_created_by and has_updated_by:
            print(f"✓ {model_name} has all timestamp fields")
        else:
            print(f"✗ {model_name} missing timestamp fields")
            print(f"  created_at: {has_created_at}, updated_at: {has_updated_at}")
            print(f"  created_by: {has_created_by}, updated_by: {has_updated_by}")
            return False
    
    return True


def test_timestamp_helper_method():
    """Test the get_timestamp_fields helper method"""
    print("\nTesting timestamp helper method...")
    
    # Create a mock instance to test the helper method
    class MockModel(TimestampedDocument):
        meta = {'abstract': True}
    
    instance = MockModel()
    
    # Manually set some timestamp data
    instance.created_at = datetime.now(timezone.utc)
    instance.updated_at = datetime.now(timezone.utc)
    instance.created_by = "test_user"
    instance.updated_by = "test_user"
    
    timestamp_data = instance.get_timestamp_fields()
    
    expected_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    for field in expected_fields:
        if field in timestamp_data:
            print(f"✓ {field} included in timestamp data")
        else:
            print(f"✗ {field} missing from timestamp data")
            return False
    
    # Check that datetime fields are properly formatted as ISO strings
    if isinstance(timestamp_data['created_at'], str):
        print("✓ created_at properly formatted as ISO string")
    else:
        print("✗ created_at not formatted as string")
        return False
    
    return True


def test_to_json_includes_timestamps():
    """Test that to_json methods include timestamp fields"""
    print("\nTesting to_json methods include timestamps...")
    
    models_with_data = [
        ('User', User, {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'Test User'
        }),
        ('Student', Student, {
            'name': 'Test Student',
            'age': 20,
            'branch': 'Computer Science'
        }),
        ('Volunteer', Volunteer, {
            'name': 'Test Volunteer',
            'contact': '1234567890',
            'availability': 'Weekends'
        })
    ]
    
    for model_name, model_class, data in models_with_data:
        instance = model_class(**data)
        
        # Manually set timestamp fields for testing
        instance.created_at = datetime.now(timezone.utc)
        instance.updated_at = datetime.now(timezone.utc)
        instance.created_by = "test_user"
        instance.updated_by = "test_user"
        
        json_data = instance.to_json()
        
        # Check that timestamp fields are included
        timestamp_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
        missing_fields = [field for field in timestamp_fields if field not in json_data]
        
        if not missing_fields:
            print(f"✓ {model_name} to_json includes all timestamp fields")
        else:
            print(f"✗ {model_name} to_json missing fields: {missing_fields}")
            return False
    
    return True


def test_abstract_base_class():
    """Test that TimestampedDocument is properly configured as abstract"""
    print("\nTesting abstract base class configuration...")
    
    if hasattr(TimestampedDocument, '_meta') and TimestampedDocument._meta.get('abstract'):
        print("✓ TimestampedDocument is properly configured as abstract")
        return True
    else:
        print("✗ TimestampedDocument is not configured as abstract")
        return False


def run_structure_tests():
    """Run all structure-based tests"""
    print("=" * 60)
    print("TIMESTAMP STRUCTURE TESTS (No MongoDB Required)")
    print("=" * 60)
    
    tests = [
        test_model_inheritance,
        test_timestamp_fields,
        test_timestamp_helper_method,
        test_to_json_includes_timestamps,
        test_abstract_base_class,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("STRUCTURE TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("🎉 All structure tests passed!")
        return True
    else:
        print("❌ Some structure tests failed. Check the errors above.")
        return False


if __name__ == "__main__":
    run_structure_tests()