from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth import auth_bp
from routes.donors import donor_bp
from routes.volunteers import volunteers_bp
from routes.users import users_bp
from routes.students import student_bp
from models import initialize_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB connection
    initialize_db(app)

    # Initialize extensions
    CORS(app)
    JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(donor_bp, url_prefix='/api/donors')
    app.register_blueprint(volunteers_bp, url_prefix='/api/volunteers')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(student_bp, url_prefix='/api/students')

    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({"message": "API Server Running"})

    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "database": "connected"})

    # 404 handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "Route not found"}), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)