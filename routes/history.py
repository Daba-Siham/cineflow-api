from werkzeug.utils import secure_filename
from uuid import uuid4
import os
from flask import Blueprint, request, jsonify, current_app, url_for

from models import history


api = Blueprint('api', __name__)


@api.get("/history/<int:user_id>")
def get_history(user_id):
    history = history.get_history_by_user(user_id)
    return jsonify(history), 200

@api.post("/history/<int:user_id>")
def add_history(user_id):
    movie_data = request.json
    history.add_history(user_id, movie_data)
    return jsonify({"message": "history added successfully"}), 201

@api.delete("/history/<int:user_id>")
def clear_history(user_id):
    history.clear_history(user_id)
    return jsonify({"message": "history cleared successfully"}), 200

