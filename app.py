from flask import Flask, request, jsonify
import sqlite3
from contextlib import closing

app = Flask(__name__)

# In-memory SQLite database connection string
DATABASE = ':memory:'

# Store the connection as a global variable to keep the in-memory DB alive
db_connection = None


def get_db():
    """Get database connection, creating it if it doesn't exist."""
    global db_connection
    if db_connection is None:
        db_connection = sqlite3.connect(DATABASE, check_same_thread=False)
        db_connection.row_factory = sqlite3.Row
        init_db()
    return db_connection


def init_db():
    """Initialize the database with users table."""
    db = get_db()
    with closing(db.cursor()) as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER
            )
        ''')
        db.commit()


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400
    
    db = get_db()
    try:
        with closing(db.cursor()) as cursor:
            cursor.execute(
                'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
                (data['name'], data['email'], data.get('age'))
            )
            db.commit()
            user_id = cursor.lastrowid
        
        return jsonify({
            'id': user_id,
            'name': data['name'],
            'email': data['email'],
            'age': data.get('age')
        }), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409


@app.route('/users', methods=['GET'])
def get_users():
    """Get all users."""
    db = get_db()
    with closing(db.cursor()) as cursor:
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
    
    return jsonify([dict(user) for user in users]), 200


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID."""
    db = get_db()
    with closing(db.cursor()) as cursor:
        cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
        user = cursor.fetchone()
    
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(dict(user)), 200


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    db = get_db()
    
    # Check if user exists
    with closing(db.cursor()) as cursor:
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
    
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    # Update user
    name = data.get('name', user['name'])
    email = data.get('email', user['email'])
    age = data.get('age', user['age'])
    
    try:
        with closing(db.cursor()) as cursor:
            cursor.execute(
                'UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?',
                (name, email, age, user_id)
            )
            db.commit()
        
        return jsonify({
            'id': user_id,
            'name': name,
            'email': email,
            'age': age
        }), 200
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    db = get_db()
    
    # Check if user exists
    with closing(db.cursor()) as cursor:
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
    
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    # Delete user
    with closing(db.cursor()) as cursor:
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        db.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/', methods=['GET'])
def index():
    """Root endpoint."""
    return jsonify({
        'message': 'Users API',
        'endpoints': {
            'GET /users': 'Get all users',
            'GET /users/<id>': 'Get a specific user',
            'POST /users': 'Create a new user',
            'PUT /users/<id>': 'Update a user',
            'DELETE /users/<id>': 'Delete a user'
        }
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5150)

