from flask import Blueprint, request, jsonify
from config.database import mongo
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required

student_bp = Blueprint('students', __name__)

def serialize_document(doc):
    """
    Converts MongoDB document ObjectId fields to strings for JSON serialization.
    Adds an 'id' field that mirrors the '_id' field.
    """
    if not doc:
        return doc
    if "_id" in doc:
        doc["id"] = str(doc["_id"])  # Add 'id' field
        doc["_id"] = str(doc["_id"])  # Convert '_id' to string
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc

@student_bp.route('/', methods=['GET'])
@jwt_required()
def get_students():
    try:
        students = list(mongo.db.students.find())
        # Serialize each student document
        students = [serialize_document(student) for student in students]
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"message": "Error retrieving students", "error": str(e)}), 500
    
@student_bp.route('/', methods=['POST'])
@jwt_required()
def create_student():
    try:
        data = request.get_json()
        result = mongo.db.students.insert_one(data)
        student_id = str(result.inserted_id)

        student = mongo.db.students.find_one({"_id": ObjectId(student_id)})
        student = serialize_document(student)

        return jsonify({
            "message": "Student created successfully",
            "student": student
        }), 201
    except Exception as e:
        return jsonify({"message": "Error creating student", "error": str(e)}), 500
    
    
@student_bp.route('/<student_id>', methods=['GET'])
@jwt_required()
def get_student_by_id(student_id):
    try:
        student = mongo.db.students.find_one({"_id": ObjectId(student_id)})
        if not student:
            return jsonify({"error": "Student not found"}), 404
        
        student = serialize_document(student)
        return jsonify(student), 200
    except Exception as e:
        return jsonify({"message": "Error retrieving student", "error": str(e)}), 500

@student_bp.route('/<student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    try:
        data = request.get_json()
        result = mongo.db.students.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": data}
        )
        
        if result.modified_count == 0:
            return jsonify({"error": "Student not found"}), 404
        
        # Get the updated document
        student = mongo.db.students.find_one({"_id": ObjectId(student_id)})
        student = serialize_document(student)
        
        return jsonify({
            "message": "Student updated successfully",
            "student": student
        }), 200
    except Exception as e:
        return jsonify({"message": "Error updating student", "error": str(e)}), 500

@student_bp.route('/<student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    try:
        result = mongo.db.students.delete_one({"_id": ObjectId(student_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Student not found"}), 404
        
        return jsonify({"message": "Student deleted"}), 200
    except Exception as e:
        return jsonify({"message": "Error deleting student", "error": str(e)}), 500