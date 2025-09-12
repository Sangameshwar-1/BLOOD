# BLOOD Project - Flask MongoDB Backend API

A robust Flask-based RESTful API with MongoDB integration for managing users, students, donors, and volunteers, secured with JWT authentication.

---

## 🚀 Features

- **JWT Authentication:** Secure user registration and login
- **MongoDB Integration:** Flexible NoSQL data storage
- **RESTful API:** Clean, consistent API endpoints
- **CORS Support:** Cross-origin resource sharing enabled
- **User Management:** Full CRUD for users
- **Student Management:** Manage student records
- **Donor Management:** Handle donor information
- **Volunteer Management:** Track volunteer details

---

## 📋 Prerequisites

- **Python 3.9+**
- **MongoDB** (local or [MongoDB Atlas](https://www.mongodb.com/atlas))
- **pip** (Python package manager)

---

## 🛠️ Installation

### 1. Clone the Project

```bash
git clone https://github.com/Sangameshwar-1/BLOOD.git
cd BLOOD/backend
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MongoDB

#### Local MongoDB (Ubuntu example)

```bash
sudo apt-get update
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
sudo systemctl status mongodb
```

#### Or use MongoDB Atlas

- [Sign up and create a cluster](https://www.mongodb.com/atlas)
- Get the connection string (e.g. `mongodb+srv://<username>:<password>@cluster.mongodb.net/<dbname>?retryWrites=true&w=majority`)

### 5. Configure Environment Variables

Create a `.env` file in your `backend` directory:

```env
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
MONGODB_URI=mongodb://localhost:27017/blood
MONGODB_DB=blood
FLASK_DEBUG=1
```

Change as needed for Atlas and production.

---

## 🚀 Quick Start

### Option 1: Using the Startup Script

```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Startup

```bash
source venv/bin/activate
export FLASK_DEBUG=1
export SECRET_KEY="local-development-secret"
export JWT_SECRET_KEY="local-jwt-secret"
export MONGODB_URI="mongodb://localhost:27017/blood"
export MONGODB_DB="blood"
python run.py
```

Server starts at `http://localhost:5000`

---

## 📊 API Endpoints

### Authentication

| Method | Endpoint            | Description                  |
|--------|---------------------|------------------------------|
| POST   | `/api/auth/register`| Register new user            |
| POST   | `/api/auth/login`   | User login                   |
| GET    | `/api/auth/me`      | Get current user (protected) |

### Users

| Method | Endpoint              | Description                  |
|--------|-----------------------|------------------------------|
| GET    | `/api/users/`         | Get all users (protected)    |
| GET    | `/api/users/details`  | Get user details (protected) |
| POST   | `/api/users/details`  | Add user details (protected) |

### Students

| Method | Endpoint                | Description                  |
|--------|-------------------------|------------------------------|
| GET    | `/api/students/`        | Get all students (protected) |
| POST   | `/api/students/`        | Create student (protected)   |
| GET    | `/api/students/{id}`    | Get student by ID (protected)|
| PUT    | `/api/students/{id}`    | Update student (protected)   |
| DELETE | `/api/students/{id}`    | Delete student (protected)   |

### Donors

| Method | Endpoint                          | Description                  |
|--------|-----------------------------------|------------------------------|
| GET    | `/api/donors/`                    | Get all donors (protected)   |
| POST   | `/api/donors/`                    | Create donor (protected)     |
| GET    | `/api/donors/user/{user_id}`      | Get donor by user ID         |
| DELETE | `/api/donors/{id}`                | Delete donor (protected)     |

### Volunteers

| Method | Endpoint                    | Description                  |
|--------|-----------------------------|------------------------------|
| GET    | `/api/volunteers/`          | Get all volunteers (protected)|
| POST   | `/api/volunteers/`          | Create volunteer (protected) |
| GET    | `/api/volunteers/{id}`      | Get volunteer by ID          |
| PUT    | `/api/volunteers/{id}`      | Update volunteer             |
| DELETE | `/api/volunteers/{id}`      | Delete volunteer             |

---

## 🔧 Testing

### Run Basic Tests

```bash
python test_simple.py
python test_db.py
python test_api_endpoints.py
python test.py
```

### Manual Testing with curl

```bash
# Server status
curl http://localhost:5000/
curl http://localhost:5000/health

# Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User","contact":"1234567890","address":"Test Address"}'

# Login user
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Use JWT token for protected endpoints
export JWT_TOKEN="your-jwt-token-here"
curl -H "Authorization: Bearer $JWT_TOKEN" http://localhost:5000/api/auth/me
```

---

## 🗃️ Database Schema

### User

- email: String, required, unique
- password: String, required
- name: String
- contact: String
- address: String

### Student

- name: String, required
- age: Int, required
- branch: String, required

### Donor

- user_id: Reference to User, required
- name: String, required
- blood_type: String, required
- contact: String, required
- address: String, required

### Volunteer

- name: String, required
- contact: String, required
- availability: String, required

---

## 🔒 Authentication

Protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

---

## 🐛 Troubleshooting

### Common Issues

**MongoDB Connection Error**

```bash
sudo systemctl start mongodb
sudo systemctl status mongodb
```

**Port 5000 Already in Use**

```bash
lsof -i :5000
kill -9 <PID>
# Or change port in run.py
```

**Python Virtual Environment Issues**

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Module Not Found Errors**

```bash
pwd   # Ensure you're in the backend directory
pip install -r requirements.txt
```

### Debug Mode

- FLASK_DEBUG=1 gives auto-reload, error messages, debugger PIN.

---

## 📁 Project Structure

```
backend/
├── app.py              # Main Flask application
├── run.py              # Application runner
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── start.sh            # Startup script
├── .env                # Environment variables (create this)
├── config/
│   ├── __init__.py
│   └── database.py     # MongoDB configuration
├── models/
│   ├── __init__.py
│   ├── user.py         # User model
│   ├── student.py      # Student model
│   ├── donor.py        # Donor model
│   └── volunteer.py    # Volunteer model
├── routes/
│   ├── auth.py         # Authentication routes
│   ├── users.py        # User routes
│   ├── students.py     # Student routes
│   ├── donors.py       # Donor routes
│   └── volunteers.py   # Volunteer routes
├── middleware/
│   └── auth.py         # Authentication middleware
└── test_*.py           # Various test files
```

---

## 🚀 Production Deployment

1. Set `FLASK_DEBUG=0` in `.env`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Use MongoDB Atlas for cloud DB
4. Set strong secret keys in `.env`
5. Enable HTTPS with SSL certificate
6. Use environment-specific config

---

## 📞 Support

- Ensure MongoDB is running (`sudo systemctl status mongodb`)
- Check dependencies: `pip list`
- Review server logs for errors
- Verify environment variables are set

---

**Happy Coding!** 🎉 Your BLOOD backend API is ready for frontend integration.
