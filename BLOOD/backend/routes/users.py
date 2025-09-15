from flask import Blueprint, request, jsonify
from config.database import mongo
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required
from middleware.auth import authenticate_token
from models.user import User

users_bp = Blueprint('users', __name__)

# Utility function to serialize MongoDB documents
def serialize_document(doc):
    """
    Converts MongoDB document ObjectId fields to strings for JSON serialization.
    Adds an 'id' field that mirrors the '_id' field.
    """
    if not doc:
        return doc
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
        doc["id"] = doc["_id"]  # Add 'id' field
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc

@users_bp.route('/details', methods=['POST'])
@authenticate_token
def add_user():
    try:
        data = request.get_json()
        user = User(**data)
        user.hash_password()
        user.save()
        return jsonify({
            "message": "User added successfully", 
            "user": user.to_json()
        }), 201
    except Exception as e:
        return jsonify({"message": "Error adding user", "error": str(e)}), 400

@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = list(mongo.db.users.find())
        # Serialize each user document
        users = [serialize_document(user) for user in users]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"message": "Error fetching users", "error": str(e)}), 500
    
@users_bp.route('/details', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        users = list(mongo.db.users.find())
        # Serialize each user document
        users = [serialize_document(user) for user in users]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"message": "Error fetching users", "error": str(e)}), 500
