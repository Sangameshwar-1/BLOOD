# config/database.py
from pymongo import MongoClient
import os

# Use environment variable or default to local MongoDB
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('MONGODB_DB', 'food2')

client = MongoClient(MONGODB_URI)
mongo = client[DB_NAME]