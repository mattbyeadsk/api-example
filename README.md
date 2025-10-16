# Users API - Flask CRUD Application

A simple Flask REST API that performs CRUD operations on a users table using an in-memory SQLite database.

## Features

- **Create** new users
- **Read** all users or a specific user by ID
- **Update** existing users
- **Delete** users
- In-memory SQLite database
- RESTful API design
- JSON request/response format

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Make sure your virtual environment is activated, then start the Flask development server:
```bash
python app.py
```

The API will be available at `http://localhost:5150`

## API Endpoints

### Root
- **GET /** - Get API information and available endpoints

### Create User
- **POST /users**
- Request body:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30
}
```
- Response: `201 Created`

### Get All Users
- **GET /users**
- Response: Array of user objects

### Get User by ID
- **GET /users/{id}**
- Response: Single user object or `404 Not Found`

### Update User
- **PUT /users/{id}**
- Request body (all fields optional):
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "age": 25
}
```
- Response: Updated user object or `404 Not Found`

### Delete User
- **DELETE /users/{id}**
- Response: Success message or `404 Not Found`

## Example Usage with curl

Create a user:
```bash
curl -X POST http://localhost:5150/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com", "age": 25}'
```

Get all users:
```bash
curl http://localhost:5150/users
```

Get a specific user:
```bash
curl http://localhost:5150/users/1
```

Update a user:
```bash
curl -X PUT http://localhost:5150/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Smith", "age": 26}'
```

Delete a user:
```bash
curl -X DELETE http://localhost:5150/users/1
```

## Database Schema

The `users` table has the following structure:

| Column | Type    | Constraints          |
|--------|---------|----------------------|
| id     | INTEGER | PRIMARY KEY AUTOINCREMENT |
| name   | TEXT    | NOT NULL             |
| email  | TEXT    | NOT NULL, UNIQUE     |
| age    | INTEGER | Optional             |

## Notes

- The database is in-memory, so all data will be lost when the application stops
- The email field must be unique
- Name and email are required fields; age is optional

