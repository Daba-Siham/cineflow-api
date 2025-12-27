# app.py
import os
from flask import Flask, send_from_directory
from routes import auth, favorites, history
from database import init_db

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# blueprints
app.register_blueprint(auth.api, url_prefix="/api/auth")
app.register_blueprint(favorites.api, url_prefix="/api/favorites")
app.register_blueprint(history.api, url_prefix="/api/history")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
