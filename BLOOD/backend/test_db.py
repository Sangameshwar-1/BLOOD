import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app
from config.database import mongo
from models.user import User
from bson.objectid import ObjectId
from flask_bcrypt import generate_password_hash

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("Testing MongoDB connection...")
    try:
        # Test connection
        collections = mongo.db.list_collection_names()
        print(f"✓ Connected to MongoDB successfully")
        print(f"✓ Database: {mongo.db.name}")
        print(f"✓ Collections: {collections}")
        return True
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False

def test_user_model():
    """Test User model operations"""
    print("\nTesting User model operations...")
    try:
        # Create test user
        test_user = User(
            email="test@example.com",
            password="testpassword",
            name="Test User",
            contact="1234567890",
            address="Test Address"
        )
        test_user.hash_password()
        test_user.save()
        
        print(f"✓ User created successfully: {test_user.email}")
        
        # Retrieve user
        retrieved_user = User.objects(email="test@example.com").first()
        if retrieved_user:
            print(f"✓ User retrieved successfully: {retrieved_user.email}")
            
            # Test password check
            if retrieved_user.check_password("testpassword"):
                print("✓ Password verification works correctly")
            else:
                print("✗ Password verification failed")
                
            # Clean up
            retrieved_user.delete()
            print("✓ Test user cleaned up")
        else:
            print("✗ Failed to retrieve user")
            
        return True
    except Exception as e:
        print(f"✗ User model test failed: {e}")
        return False

def test_student_collection():
    """Test students collection operations"""
    print("\nTesting students collection operations...")
    try:
        # Test insert
        student_data = {
            "name": "John Doe",
            "age": 20,
            "branch": "Computer Science"
        }
        
        result = mongo.db.students.insert_one(student_data)
        student_id = str(result.inserted_id)
        print(f"✓ Student inserted successfully: {student_id}")
        
        # Test find
        student = mongo.db.students.find_one({"_id": ObjectId(student_id)})
        if student:
            print(f"✓ Student retrieved successfully: {student['name']}")
            
            # Test update
            update_result = mongo.db.students.update_one(
                {"_id": ObjectId(student_id)},
                {"$set": {"age": 21}}
            )
            if update_result.modified_count > 0:
                print("✓ Student updated successfully")
            
            # Test delete
            delete_result = mongo.db.students.delete_one({"_id": ObjectId(student_id)})
            if delete_result.deleted_count > 0:
                print("✓ Student deleted successfully")
            else:
                print("✗ Failed to delete student")
        else:
            print("✗ Failed to retrieve student")
            
        return True
    except Exception as e:
        print(f"✗ Students collection test failed: {e}")
        return False

def test_donor_collection():
    """Test donors collection operations"""
    print("\nTesting donors collection operations...")
    try:
        # Test insert
        donor_data = {
            "name": "Jane Smith",
            "blood_type": "O+",
            "contact": "9876543210",
            "address": "Donor Address"
        }
        
        result = mongo.db.donors.insert_one(donor_data)
        donor_id = str(result.inserted_id)
        print(f"✓ Donor inserted successfully: {donor_id}")
        
        # Test find
        donor = mongo.db.donors.find_one({"_id": ObjectId(donor_id)})
        if donor:
            print(f"✓ Donor retrieved successfully: {donor['name']}")
            
            # Clean up
            delete_result = mongo.db.donors.delete_one({"_id": ObjectId(donor_id)})
            if delete_result.deleted_count > 0:
                print("✓ Donor cleaned up successfully")
        else:
            print("✗ Failed to retrieve donor")
            
        return True
    except Exception as e:
        print(f"✗ Donors collection test failed: {e}")
        return False

def test_all_collections():
    """Test all collections"""
    print("=" * 50)
    print("DATABASE TESTING SCRIPT")
    print("=" * 50)
    
    # Create app context for MongoEngine operations
    app = create_app()
    
    with app.app_context():
        results = []
        
        # Run all tests
        results.append(test_mongodb_connection())
        results.append(test_user_model())
        results.append(test_student_collection())
        results.append(test_donor_collection())
        
        # Summary
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        print(f"Total tests: {len(results)}")
        print(f"Passed: {sum(results)}")
        print(f"Failed: {len(results) - sum(results)}")
        
        if all(results):
            print("🎉 All database tests passed!")
            return True
        else:
            print("❌ Some tests failed. Check the errors above.")
            return False

if __name__ == "__main__":
    test_all_collections()