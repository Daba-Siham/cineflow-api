from database import get_connection


def get_history_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM history WHERE user_id = ? ORDER BY timestamp DESC', (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history

def add_history(user_id, movie_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO history (
            user_id, imdb_id, title, year, Rated, released, runtime, genre,
            director, writer, actors, plot, language, country, awards,
            poster, ratings, metascore, imdbRating, imdbVotes, type
        ) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'', (
            user_id,
            movie_data['imdbID'],
            movie_data['Title'],
            movie_data['Year'],
            movie_data['Rated'],
            movie_data['Released'],
            movie_data['Runtime'],
            movie_data['Genre'],
            movie_data['Director'],
            movie_data['Writer'],
            movie_data['Actors'],
            movie_data['Plot'],
            movie_data['Language'],
            movie_data['Country'],
            movie_data['Awards'],
            movie_data['Poster'],
            str(movie_data.get('Ratings', [])),
            movie_data.get('Metascore', ''),
            movie_data.get('imdbRating', ''),
            movie_data.get('imdbVotes', ''),
            movie_data.get('Type', '')
        )
    ''')

    conn.commit()
    conn.close()

def clear_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM history WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

