from flask import Blueprint, request, jsonify
from config.database import mongo
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required

donor_bp = Blueprint('donors', __name__)

def serialize_document(doc):
    """Converts MongoDB ObjectId fields to strings for JSON serialization."""
    if not doc:
        return doc
    if "_id" in doc:
        doc["id"] = str(doc["_id"])  # Add an 'id' field
        doc["_id"] = str(doc["_id"])  # Convert '_id' to string
    return doc

@donor_bp.route('/', methods=['POST'])
@jwt_required()
def create_donor():
    try:
        data = request.get_json()
        result = mongo.db.donors.insert_one(data)
        donor_id = str(result.inserted_id)

        donor = mongo.db.donors.find_one({"_id": ObjectId(donor_id)})
        donor = serialize_document(donor)

        return jsonify({
            "message": "Donor created successfully",
            "donor": donor
        }), 201
    except Exception as e:
        return jsonify({"message": "Error creating donor", "error": str(e)}), 500
    
# Get all donors
@donor_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_donors():
    try:
        donors = list(mongo.db.donors.find())
        # Serialize each donor document
        donors = [serialize_document(donor) for donor in donors]
        return jsonify(donors), 200
    except Exception as e:
        return jsonify({"message": "Error fetching donors", "error": str(e)}), 500

# Get a donor by user ID
@donor_bp.route('/user/<user_id>', methods=['GET'])
@jwt_required()
def get_donor_by_user_id(user_id):
    try:
        donor = mongo.db.donors.find_one({"userId": ObjectId(user_id)})
        if not donor:
            return jsonify({"message": "Donor not found"}), 404

        # Serialize the donor document
        donor = serialize_document(donor)

        return jsonify(donor), 200
    except Exception as e:
        return jsonify({"message": "Error fetching donor details", "error": str(e)}), 500
    
@donor_bp.route('/<donor_id>', methods=['DELETE'])
@jwt_required()
def delete_donor(donor_id):
    try:
        # Convert donor_id to ObjectId
        donor = mongo.db.donors.find_one({"_id": ObjectId(donor_id)})
        if not donor:
            return jsonify({"message": "Donor not found"}), 404

        # Delete the donor
        mongo.db.donors.delete_one({"_id": ObjectId(donor_id)})
        return jsonify({"message": "Donor deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error deleting donor", "error": str(e)}), 500