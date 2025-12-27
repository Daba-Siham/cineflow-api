# models/favorites.py
from database import get_connection

def get_favorites_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM favoris WHERE user_id = ? ORDER BY timestamp DESC",
        (user_id,),
    )
    rows = cursor.fetchall()
    conn.close()

    # on transforme en liste de dict pour pouvoir faire jsonify()
    return [dict(row) for row in rows]


def add_favorite(user_id, movie_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO favoris (
            user_id, imdb_id, title, year, Rated, released, runtime, genre,
            director, writer, actors, plot, language, country, awards,
            poster, ratings, metascore, imdbRating, imdbVotes, type
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            user_id,
            movie_data.get("imdbID"),
            movie_data.get("Title"),
            movie_data.get("Year"),
            movie_data.get("Rated"),
            movie_data.get("Released"),
            movie_data.get("Runtime"),
            movie_data.get("Genre"),
            movie_data.get("Director"),
            movie_data.get("Writer"),
            movie_data.get("Actors"),
            movie_data.get("Plot"),
            movie_data.get("Language"),
            movie_data.get("Country"),
            movie_data.get("Awards"),
            movie_data.get("Poster"),
            str(movie_data.get("Ratings", [])),
            movie_data.get("Metascore", ""),
            movie_data.get("imdbRating", ""),
            movie_data.get("imdbVotes", ""),
            movie_data.get("Type", ""),
        ),
    )
    conn.commit()
    conn.close()


def remove_favorite(user_id, imdb_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM favoris WHERE user_id = ? AND imdb_id = ?",
        (user_id, imdb_id),
    )
    conn.commit()
    conn.close()

def clear_favorites(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM favoris WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()