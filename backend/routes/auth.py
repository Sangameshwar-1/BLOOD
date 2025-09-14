from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_bcrypt import check_password_hash
from models.user import User
from middleware.auth import authenticate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    
    if User.objects(email=email).first():
        return jsonify({"message": "User already exists"}), 409
    
    try:
        new_user = User(
            email=email,
            password=password,
            name=data.get('name', ''),
            contact=data.get('contact', ''),
            address=data.get('address', '')
        )
        new_user.hash_password()
        new_user.save()
        
        return jsonify({
            "message": "Registration successful", 
            "user": {"id": str(new_user.id), "email": new_user.email}
        }), 201
    except Exception as e:
        return jsonify({"message": "Error registering user", "error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print("Login request data:", data)  # Debug log
        email = data.get("email")
        password = data.get("password")

        user = User.objects(email=email).first()
        if not user:
            print("User not found")  # Debug log
            return jsonify({"message": "Invalid credentials"}), 401

        if not user.check_password(password):
            print("Invalid password")  # Debug log
            return jsonify({"message": "Invalid credentials"}), 401

        access_token = create_access_token(identity=str(user.id))
        print("Access token generated:", access_token)  # Debug log
        return jsonify({"token": access_token}), 200
    except Exception as e:
        print("Error logging in:", str(e))  # Debug log
        return jsonify({"message": "Error logging in", "error": str(e)}), 500
    

@auth_bp.route('/me', methods=['GET'])
@authenticate_token
def get_me():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        return jsonify({
            "id": str(user.id), 
            "email": user.email, 
            "name": user.name
        })
    except Exception as e:
        return jsonify({"message": "Server error", "error": str(e)}), 500