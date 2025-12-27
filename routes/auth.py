# routes/auth.py
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
from flask import Blueprint, request, jsonify, current_app
import sqlite3  
from models import auth

api = Blueprint("auth_api", __name__)  


@api.post("/register")
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password_hash = request.form.get("password_hash")

    if not username or not email or not password_hash:
        return jsonify({"message": "Missing fields"}), 400

    if auth.get_user_by_username(username):
        return jsonify({"message": "Username already exists"}), 400

    if auth.get_user_by_email(email):
        return jsonify({"message": "Email already exists"}), 400

    try:
        auth.register_user(username, email, password_hash)
    except sqlite3.IntegrityError as e:
        if "users.email" in str(e):
            return jsonify({"message": "Email already exists"}), 400
        if "users.username" in str(e):
            return jsonify({"message": "Username already exists"}), 400
        return jsonify({"message": "Database error"}), 500

    user = auth.get_user_by_username(username)

    file = request.files.get("image")
    if file and file.filename != "":
        filename = secure_filename(file.filename)
        unique_name = f"{uuid4().hex}_{filename}"

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        save_path = os.path.join(upload_folder, unique_name)
        file.save(save_path)

        rel_path = f"/uploads/{unique_name}"
        auth.upload_profile_picture(user["id"], rel_path)

    user = auth.get_user_by_id(user["id"])

    user_data = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "imgProfile": user["imgProfile"],
        "created_at": user["created_at"],
    }

    return jsonify(user_data), 201

# @api.post("/login")
# def login():
#     data = request.json
#     username = data.get("username")
#     password_hash = data.get("password_hash")

#     if auth.verify_user(username, password_hash):
#         return jsonify({"message": "Login successful"}), 200
#     else:
#         return jsonify({"message": "Invalid credentials"}), 401


@api.put("/update_password/<int:user_id>")
def update_password(user_id):
    data = request.json
    new_password_hash = data.get("new_password_hash")

    auth.update_password(user_id, new_password_hash)
    return jsonify({"message": "Password updated successfully"}), 200


@api.put("/update_email/<int:user_id>")
def update_email(user_id):
    data = request.json
    new_email = data.get("new_email")

    auth.update_email(user_id, new_email)
    return jsonify({"message": "Email updated successfully"}), 200


@api.get("/user/<int:user_id>")
def get_user(user_id):
    user = auth.get_user_by_id(user_id)
    if user:
        user_data = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "imgProfile": user["imgProfile"],
            "created_at": user["created_at"],
        }
        return jsonify(user_data), 200
    else:
        return jsonify({"message": "User not found"}), 404


@api.post("/login_user")
def login_user():
    data = request.json
    username = data.get("username")
    password_hash = data.get("password_hash")

    user = auth.login_user(username, password_hash)
    if user:
        user_data = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "imgProfile": user["imgProfile"],
            "created_at": user["created_at"],
        }
        return jsonify(user_data), 200
    else:
        return jsonify({"message": "Nom d'utilisateur ou mot de passe incorrect"}), 404


@api.get("/verify_user/<string:username>/<string:password_hash>")
def verify_user(username, password_hash):
    if auth.verify_user(username, password_hash):
        return jsonify({"message": "User verified"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@api.post("/upload_profile_image/<int:user_id>")
def upload_profile_image(user_id):
    if "image" not in request.files:
        return jsonify({"message": "no file"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"message": "empty filename"}), 400

    filename = secure_filename(file.filename)
    unique_name = f"{uuid4().hex}_{filename}"

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    save_path = os.path.join(upload_folder, unique_name)
    file.save(save_path)

    rel_path = f"/uploads/{unique_name}"
    auth.upload_profile_picture(user_id, rel_path)

    return jsonify(
        {
            "filename": unique_name,
            "path": rel_path,
        }
    ), 201
