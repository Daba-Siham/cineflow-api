# routes/favorites.py
from flask import Blueprint, request, jsonify
from models import favorites  

api = Blueprint("favorites_api", __name__)  # nom unique


@api.get("/<int:user_id>")
def get_favorites(user_id):
    favs = favorites.get_favorites_by_user(user_id)
    return jsonify(favs), 200


@api.get("/<int:user_id>/<string:imdb_id>")
def is_favorite(user_id, imdb_id):
    favs = favorites.get_favorites_by_user(user_id)
    is_fav = any(fav["imdb_id"] == imdb_id for fav in favs)
    if is_fav:
        return jsonify({"is_favorite": True}), 200
    else:
        return jsonify({"is_favorite": False}), 404


@api.post("/<int:user_id>")
def add_favorite(user_id):
    movie_data = request.json
    favorites.add_favorite(user_id, movie_data)
    return jsonify({"message": "Favorite added successfully"}), 201


@api.delete("/<int:user_id>/<string:imdb_id>")
def remove_favorite(user_id, imdb_id):
    favorites.remove_favorite(user_id, imdb_id)
    return jsonify({"message": "Favorite removed successfully"}), 200

@api.delete("/clear/<int:user_id>")
def clear_favorites(user_id):
    favorites.clear_favorites(user_id)
    return jsonify({"message": "All favorites cleared successfully"}), 200