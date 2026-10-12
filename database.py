import sqlite3
import json
from datetime import datetime
import os

DATABASE_PATH = os.environ.get("DATABASE_PATH", "chat_app.db")

def get_db_connection():
    """Get database connection with row factory for dict-like access"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Rooms table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            owner TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT NOT NULL,
            username TEXT NOT NULL,
            content TEXT,
            file_name TEXT,
            file_extension TEXT,
            file_type TEXT,
            file_size TEXT,
            file_binary TEXT,
            is_file BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_name) REFERENCES rooms(name)
        )
    ''')
    
    conn.commit()
    conn.close()

# User functions
def create_user(username, password):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                      (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Username already exists

def get_user(username):
    """Get user by username"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def user_exists(username):
    """Check if user exists"""
    return get_user(username) is not None

# Room functions
def create_room(room_name, owner):
    """Create a new room"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO rooms (name, owner) VALUES (?, ?)', 
                      (room_name, owner))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Room already exists

def get_all_rooms():
    """Get all room names"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM rooms ORDER BY created_at DESC')
    rooms = cursor.fetchall()
    conn.close()
    return [room['name'] for room in rooms]

def room_exists(room_name):
    """Check if room exists"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM rooms WHERE name = ?', (room_name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def search_rooms(query):
    """Search rooms by name"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM rooms WHERE name LIKE ? ORDER BY created_at DESC', 
                  (f'%{query}%',))
    rooms = cursor.fetchall()
    conn.close()
    return [room['name'] for room in rooms]

def get_room_owner(room_name):
    """Get room owner"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT owner FROM rooms WHERE name = ?', (room_name,))
    result = cursor.fetchone()
    conn.close()
    return result['owner'] if result else None

def delete_room(room_name):
    """Delete a room and all its messages"""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Delete messages first (foreign key constraint)
    cursor.execute('DELETE FROM messages WHERE room_name = ?', (room_name,))
    # Delete room
    cursor.execute('DELETE FROM rooms WHERE name = ?', (room_name,))
    conn.commit()
    conn.close()

# Message functions
def add_message(room_name, username, content=None, file_data=None):
    """Add a message to a room"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if file_data:
        # File message
        cursor.execute('''
            INSERT INTO messages 
            (room_name, username, file_name, file_extension, file_type, file_size, file_binary, is_file)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        ''', (room_name, username, file_data.get('name'), file_data.get('extension'), 
              file_data.get('type'), file_data.get('size'), file_data.get('binary')))
    else:
        # Text message
        cursor.execute('''
            INSERT INTO messages (room_name, username, content, is_file)
            VALUES (?, ?, ?, 0)
        ''', (room_name, username, content))
    
    # Get the inserted message ID
    message_id = cursor.lastrowid
    
    # Fetch the complete message with timestamp
    cursor.execute('SELECT * FROM messages WHERE id = ?', (message_id,))
    message = cursor.fetchone()
    
    conn.commit()
    conn.close()
    
    # Format message for frontend
    formatted_message = {
        'user': message['username'],
        'created': message['created_at']
    }
    
    if message['is_file']:
        formatted_message.update({
            'extention': message['file_extension'],
            'name': message['file_name'],
            'type': message['file_type'],
            'size': message['file_size'],
            'binary': message['file_binary']
        })
    else:
        formatted_message['content'] = message['content']
    
    return formatted_message

def get_room_messages(room_name):
    """Get all messages for a room"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM messages 
        WHERE room_name = ? 
        ORDER BY created_at ASC
    ''', (room_name,))
    messages = cursor.fetchall()
    conn.close()
    
    # Format messages for frontend
    formatted_messages = []
    for msg in messages:
        formatted_msg = {
            'user': msg['username'],
            'created': msg['created_at']
        }
        
        if msg['is_file']:
            formatted_msg.update({
                'extention': msg['file_extension'],
                'name': msg['file_name'],
                'type': msg['file_type'],
                'size': msg['file_size'],
                'binary': msg['file_binary']
            })
        else:
            formatted_msg['content'] = msg['content']
        
        formatted_messages.append(formatted_msg)
    
    return formatted_messages