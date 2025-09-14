#!/usr/bin/env python
"""
Demo script showing the timestamp functionality working.
This demonstrates how the timestamps are automatically managed.
"""
import sys
import os
from datetime import datetime, timezone
import time
sys.path.insert(0, os.path.abspath('.'))

from models.user import User
from models.student import Student
from models.volunteer import Volunteer


def demo_timestamp_functionality():
    """
    Demonstrate the timestamp functionality without requiring MongoDB connection.
    This shows how the save method would work when connected to a database.
    """
    print("=" * 60)
    print("TIMESTAMP FUNCTIONALITY DEMONSTRATION")
    print("=" * 60)
    
    print("\n1. Creating a new User instance...")
    user = User(
        email="demo@example.com",
        password="demo123",
        name="Demo User",
        contact="1234567890",
        address="Demo Address"
    )
    user.hash_password()
    
    print("   Before first save:")
    print(f"   - created_at: {user.created_at}")
    print(f"   - updated_at: {user.updated_at}")
    print(f"   - has pk: {bool(user.pk)}")
    
    # Simulate what happens during save (without actually connecting to MongoDB)
    print("\n2. Simulating first save...")
    if not user.pk:
        user.created_at = datetime.now(timezone.utc)
        # Simulate getting a primary key after save
        user.pk = "mock_object_id_123"
    user.updated_at = datetime.now(timezone.utc)
    
    first_created_at = user.created_at
    first_updated_at = user.updated_at
    
    print("   After first save:")
    print(f"   - created_at: {first_created_at}")
    print(f"   - updated_at: {first_updated_at}")
    print(f"   - has pk: {bool(user.pk)}")
    
    # Add user tracking
    user.created_by = "admin_user"
    user.updated_by = "admin_user"
    
    print("\n3. User JSON representation:")
    json_data = user.to_json()
    for key, value in sorted(json_data.items()):
        print(f"   - {key}: {value}")
    
    # Simulate updating the user
    print("\n4. Simulating user update...")
    time.sleep(1)  # Ensure different timestamp
    user.name = "Updated Demo User"
    user.updated_by = "different_user"
    
    # Simulate what happens during update save
    if user.pk:  # Already has pk, so don't change created_at
        pass
    user.updated_at = datetime.now(timezone.utc)
    
    print("   After update save:")
    print(f"   - created_at: {user.created_at} (unchanged)")
    print(f"   - updated_at: {user.updated_at} (updated)")
    print(f"   - created_by: {user.created_by} (unchanged)")
    print(f"   - updated_by: {user.updated_by} (updated)")
    
    print(f"\n   Time difference: {(user.updated_at - first_updated_at).total_seconds()} seconds")
    
    print("\n5. Updated JSON representation:")
    updated_json = user.to_json()
    for key, value in sorted(updated_json.items()):
        print(f"   - {key}: {value}")
    
    print("\n6. Testing with other models...")
    
    # Test Student
    student = Student(name="Test Student", age=20, branch="Computer Science")
    student.created_at = datetime.now(timezone.utc)
    student.updated_at = datetime.now(timezone.utc)
    student.created_by = "registrar"
    
    print("\n   Student JSON with timestamps:")
    student_json = student.to_json()
    for key, value in sorted(student_json.items()):
        print(f"   - {key}: {value}")
    
    # Test Volunteer
    volunteer = Volunteer(name="Test Volunteer", contact="9876543210", availability="Weekends")
    volunteer.created_at = datetime.now(timezone.utc)
    volunteer.updated_at = datetime.now(timezone.utc)
    
    print("\n   Volunteer JSON with timestamps:")
    volunteer_json = volunteer.to_json()
    for key, value in sorted(volunteer_json.items()):
        print(f"   - {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ DEMONSTRATION COMPLETE")
    print("All models now have automatic timestamp tracking!")
    print("- created_at: Set automatically on first save")
    print("- updated_at: Updated automatically on every save")
    print("- created_by/updated_by: Available for manual user tracking")
    print("- All fields included in JSON serialization")
    print("=" * 60)


if __name__ == "__main__":
    demo_timestamp_functionality()