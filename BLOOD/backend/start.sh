#!/bin/bash
# start.sh

echo "Starting Flask MongoDB Backend..."

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "MongoDB is not running. Please start MongoDB first."
    echo "Run: sudo systemctl start mongodb"
    exit 1
fi

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Set environment variables
export FLASK_DEBUG=1
export SECRET_KEY="local-development-secret"
export JWT_SECRET_KEY="local-jwt-secret"
export MONGODB_URI="mongodb://localhost:27017/food2"
export MONGODB_DB="food2"

# Run the application
echo "Starting Flask server..."
python run.py
