from flask import Blueprint, request, jsonify
from config.database import mongo  # Import the mongo object
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required
from models.volunteer import Volunteer

volunteers_bp = Blueprint('volunteers', __name__)

# Utility function to serialize MongoDB documents
def serialize_document(doc):
    """Converts MongoDB ObjectId fields to strings for JSON serialization."""
    if not doc:
        return doc
    if "_id" in doc:
        doc["id"] = str(doc["_id"])  # Add 'id' field with stringified ObjectId
        doc["_id"] = str(doc["_id"])  # Keep '_id' field as string
    return doc


@volunteers_bp.route('/', methods=['POST'])
@jwt_required()
def create_volunteer():
    try:
        data = request.get_json()
        result = mongo.db.volunteers.insert_one(data)
        volunteer_id = str(result.inserted_id)

        volunteer = mongo.db.volunteers.find_one({"_id": ObjectId(volunteer_id)})
        volunteer = serialize_document(volunteer)

        return jsonify({
            "message": "Volunteer created successfully",
            "volunteer": volunteer
        }), 201
    except Exception as e:
        return jsonify({"message": "Error creating volunteer", "error": str(e)}), 500
    
# Get all volunteers
@volunteers_bp.route('/', methods=['GET'])
@jwt_required()
def get_volunteers():
    try:
        volunteers = list(mongo.db.volunteers.find())
        # Serialize each volunteer document
        volunteers = [serialize_document(volunteer) for volunteer in volunteers]
        return jsonify(volunteers), 200
    except Exception as e:
        return jsonify({"message": "Error fetching volunteers", "error": str(e)}), 500

# Get a volunteer by ID
@volunteers_bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_volunteer(id):
    try:
        volunteer = mongo.db.volunteers.find_one({"_id": ObjectId(id)})
        if not volunteer:
            return jsonify({"message": "Volunteer not found"}), 404

        # Serialize the volunteer document
        volunteer = serialize_document(volunteer)

        return jsonify(volunteer), 200
    except Exception as e:
        return jsonify({"message": "Error fetching volunteer", "error": str(e)}), 500

# Update a volunteer by ID
@volunteers_bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update_volunteer(id):
    try:
        data = request.get_json()
        result = mongo.db.volunteers.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        if result.matched_count == 0:
            return jsonify({"message": "Volunteer not found"}), 404

        # Fetch the updated volunteer
        volunteer = mongo.db.volunteers.find_one({"_id": ObjectId(id)})
        volunteer = serialize_document(volunteer)

        return jsonify(volunteer), 200
    except Exception as e:
        return jsonify({"message": "Error updating volunteer", "error": str(e)}), 500


@volunteers_bp.route('/<volunteer_id>', methods=['DELETE'])
@jwt_required()
def delete_volunteer(volunteer_id):
    try:
        print(f"Attempting to delete volunteer with ID: {volunteer_id}")  # Debug log

        # Validate the volunteer_id
        try:
            volunteer_id = ObjectId(volunteer_id)
        except InvalidId:
            print("Invalid volunteer ID")  # Debug log
            return jsonify({"message": "Invalid volunteer ID"}), 400

        # Check if the volunteer exists
        volunteer = mongo.db.volunteers.find_one({"_id": volunteer_id})
        if not volunteer:
            print("Volunteer not found")  # Debug log
            return jsonify({"message": "Volunteer not found"}), 404

        # Delete the volunteer
        mongo.db.volunteers.delete_one({"_id": volunteer_id})
        print("Volunteer deleted successfully")  # Debug log
        return jsonify({"message": "Volunteer deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting volunteer: {e}")  # Debug log
        return jsonify({"message": "Error deleting volunteer", "error": str(e)}), 500