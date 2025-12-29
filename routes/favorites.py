from flask import Blueprint, request, jsonify
from models import favorites as favorites_model

api = Blueprint("favorites_api", __name__)


@api.get("/<int:user_id>")
def get_favorites(user_id):
    favs = favorites_model.get_favorites_by_user(user_id)
    return jsonify(favs), 200


@api.get("/<int:user_id>/<string:imdb_id>")
def is_favorite(user_id, imdb_id):
    favs = favorites_model.get_favorites_by_user(user_id)
    is_fav = any(f["imdb_id"] == imdb_id for f in favs)
    return jsonify({"is_favorite": is_fav}), 200


@api.post("/<int:user_id>")
def add_favorite(user_id):
    movie_data = request.json
    favorites_model.add_favorite(user_id, movie_data)
    return jsonify({"message": "Favorite added successfully"}), 201


@api.delete("/<int:user_id>/<string:imdb_id>")
def remove_favorite(user_id, imdb_id):
    favorites_model.remove_favorite(user_id, imdb_id)
    return jsonify({"message": "Favorite removed successfully"}), 200


@api.delete("/clear/<int:user_id>")
def clear_favorites(user_id):
    favorites_model.clear_favorites(user_id)
    return jsonify({"message": "All favorites cleared successfully"}), 200
