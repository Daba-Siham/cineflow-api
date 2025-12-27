# models/auth.py
from database import get_connection


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    return cursor.fetchone()

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(username, email, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, email, imgProfile, password_hash)
        VALUES (?, ?, ?, ?)
    """, (username, email, None, password_hash))
    conn.commit()
    conn.close()

def login_user(username, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password_hash = ?
    """, (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_user(username, password_hash):
    return login_user(username, password_hash) is not None

def update_password(user_id, new_password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET password_hash = ? WHERE id = ?
    """, (new_password_hash, user_id))
    conn.commit()
    conn.close()

def update_email(user_id, new_email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET email = ? WHERE id = ?
    """, (new_email, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def upload_profile_picture(user_id, picture_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET imgProfile = ? WHERE id = ?
    """, (picture_path, user_id))
    conn.commit()
    conn.close()

def get_profile_picture(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT imgProfile FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row["imgProfile"] if row else None
