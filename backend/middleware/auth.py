from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps

def authenticate_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            request.user = current_user
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": "Invalid or expired token"}), 401
    return decorated_function