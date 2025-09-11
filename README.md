# Flask MongoDB Backend API

A robust Flask-based RESTful API with MongoDB integration for managing users, students, donors, and volunteers with JWT authentication.

## 🚀 Features

- **JWT Authentication** - Secure user registration and login
- **MongoDB Integration** - NoSQL database for flexible data storage
- **RESTful API** - Clean and consistent API endpoints
- **CORS Support** - Cross-origin resource sharing enabled
- **User Management** - Complete CRUD operations for users
- **Student Management** - Manage student records
- **Donor Management** - Handle donor information
- **Volunteer Management** - Track volunteer details

## 📋 Prerequisites

- Python 3.9+
- MongoDB (local installation or MongoDB Atlas)
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone or download the project

```bash
cd ~/Documents/Mongodb/food2/backend
```

### 2. Set up virtual environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up MongoDB

```bash
# Install MongoDB on Ubuntu
sudo apt-get update
sudo apt-get install -y mongodb

# Start MongoDB service
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Check MongoDB status
sudo systemctl status mongodb
```

### 5. Set environment variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
MONGODB_URI=mongodb://localhost:27017/food2
MONGODB_DB=food2
FLASK_DEBUG=1
```

## 🚀 Quick Start

### Option 1: Using the startup script (Recommended)

```bash
# Make the script executable
chmod +x start.sh

# Run the application
./start.sh
```

### Option 2: Manual startup

```bash
# Activate virtual environment
source venv/bin/activate

# Set environment variables
export FLASK_DEBUG=1
export SECRET_KEY="local-development-secret"
export JWT_SECRET_KEY="local-jwt-secret"
export MONGODB_URI="mongodb://localhost:27017/food2"
export MONGODB_DB="food2"

# Run the application
python run.py
```

The server will start on `http://localhost:5000`

## 📊 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | User login |
| GET | `/api/auth/me` | Get current user (protected) |

### User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | Get all users (protected) |
| GET | `/api/users/details` | Get user details (protected) |
| POST | `/api/users/details` | Add user details (protected) |

### Student Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students/` | Get all students (protected) |
| POST | `/api/students/` | Create student (protected) |
| GET | `/api/students/{id}` | Get student by ID (protected) |
| PUT | `/api/students/{id}` | Update student (protected) |
| DELETE | `/api/students/{id}` | Delete student (protected) |

### Donor Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/donors/` | Get all donors (protected) |
| POST | `/api/donors/` | Create donor (protected) |
| GET | `/api/donors/user/{user_id}` | Get donor by user ID (protected) |
| DELETE | `/api/donors/{id}` | Delete donor (protected) |

### Volunteer Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/volunteers/` | Get all volunteers (protected) |
| POST | `/api/volunteers/` | Create volunteer (protected) |
| GET | `/api/volunteers/{id}` | Get volunteer by ID (protected) |
| PUT | `/api/volunteers/{id}` | Update volunteer (protected) |
| DELETE | `/api/volunteers/{id}` | Delete volunteer (protected) |

## 🔧 Testing

### Run basic tests

```bash
# Test basic functionality
python test_simple.py

# Test database connection
python test_db.py

# Test API endpoints
python test_api_endpoints.py

# Run comprehensive test
python test.py
```

### Manual testing with curl

```bash
# Test server status
curl http://localhost:5000/
curl http://localhost:5000/health

# Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User",
    "contact": "1234567890",
    "address": "Test Address"
  }'

# Login user
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Save the JWT token from login response and use it:
export JWT_TOKEN="your-jwt-token-here"

# Test protected endpoint
curl -H "Authorization: Bearer $JWT_TOKEN" \
  http://localhost:5000/api/auth/me
```

## 🗃️ Database Schema

### User Model
- email (String, required, unique)
- password (String, required)
- name (String)
- contact (String)
- address (String)

### Student Model
- name (String, required)
- age (Int, required)
- branch (String, required)

### Donor Model
- user_id (Reference to User, required)
- name (String, required)
- blood_type (String, required)
- contact (String, required)
- address (String, required)

### Volunteer Model
- name (String, required)
- contact (String, required)
- availability (String, required)

## 🔒 Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   ```bash
   sudo systemctl start mongodb
   sudo systemctl status mongodb
   ```

2. **Port 5000 already in use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   
   # Kill the process
   kill -9 <PID>
   
   # Or change port in run.py
   ```

3. **Python virtual environment issues**
   ```bash
   # Recreate virtual environment
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Module not found errors**
   ```bash
   # Ensure you're in the backend directory
   pwd
   
   # Reinstall requirements
   pip install -r requirements.txt
   ```

### Debug Mode

The application runs in debug mode by default (FLASK_DEBUG=1). This provides:
- Automatic reloading on code changes
- Detailed error messages
- Debugger PIN for debugging

## 📁 Project Structure

```
backend/
├── app.py                 # Main Flask application
├── run.py                # Application runner
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── start.sh             # Startup script
├── .env                 # Environment variables (create this)
├── config/
│   ├── __init__.py
│   └── database.py      # MongoDB configuration
├── models/
│   ├── __init__.py
│   ├── user.py          # User model
│   ├── student.py       # Student model
│   ├── donor.py         # Donor model
│   └── volunteer.py     # Volunteer model
├── routes/
│   ├── auth.py          # Authentication routes
│   ├── users.py         # User routes
│   ├── students.py      # Student routes
│   ├── donors.py        # Donor routes
│   └── volunteers.py    # Volunteer routes
├── middleware/
│   └── auth.py          # Authentication middleware
└── test_*.py           # Various test files
```

## 🚀 Production Deployment

For production, consider:

1. **Set FLASK_DEBUG=0** in environment variables
2. **Use a production WSGI server** (Gunicorn, uWSGI)
3. **Use MongoDB Atlas** for cloud database
4. **Set strong secret keys** in environment variables
5. **Enable HTTPS** with SSL certificate
6. **Use environment-specific configuration**

## 📞 Support

If you encounter any issues:

1. Check that MongoDB is running: `sudo systemctl status mongodb`
2. Verify all dependencies are installed: `pip list`
3. Check the server logs for error messages
4. Ensure all environment variables are set correctly


---

**Happy Coding!** 🎉 Your backend API is now ready to use with frontend applications.
