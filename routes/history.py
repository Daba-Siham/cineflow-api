from flask import Blueprint, request, jsonify
from models import history as history_model

api = Blueprint("history_api", __name__)


@api.get("/<int:user_id>")
def get_history(user_id):
    data = history_model.get_history_by_user(user_id)
    return jsonify(data), 200


@api.post("/<int:user_id>")
def add_history(user_id):
    movie_data = request.json
    history_model.add_history(user_id, movie_data)
    return jsonify({"message": "history added successfully"}), 201


@api.delete("/<int:user_id>")
def clear_history(user_id):
    history_model.clear_history(user_id)
    return jsonify({"message": "history cleared successfully"}), 200
