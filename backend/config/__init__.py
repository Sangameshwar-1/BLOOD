import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-here'
    MONGODB_DB = os.environ.get('MONGODB_DB') or 'food2'
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/food2'
    DEBUG = os.environ.get('FLASK_DEBUG') or False