import sqlite3

DB_NAME = "cineflow.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        imgProfile TEXT,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS favoris (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        imdb_id VARCHAR(20) NOT NULL,
        title TEXT,
        year TEXT,
        Rated TEXT,
        released TEXT,
        runtime TEXT,
        genre TEXT,
        director TEXT,
        writer TEXT,
        actors TEXT,
        plot TEXT,
        language TEXT,
        country TEXT,
        awards TEXT,
        poster TEXT,
        ratings TEXT,
        metascore TEXT,
        imdbRating TEXT,
        imdbVotes TEXT,
        type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        imdb_id VARCHAR(20) NOT NULL,
        title TEXT,
        year TEXT,
        Rated TEXT,
        released TEXT,
        runtime TEXT,
        genre TEXT,
        director TEXT,
        writer TEXT,
        actors TEXT,
        plot TEXT,
        language TEXT,
        country TEXT,
        awards TEXT,
        poster TEXT,
        ratings TEXT,
        metascore TEXT,
        imdbRating TEXT,
        imdbVotes TEXT,
        type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()
