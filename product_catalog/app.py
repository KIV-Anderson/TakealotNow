# app.py
from flask import Flask, redirect, url_for
import os

# Import the Database functions to set up tables on launch
from db import get_db_connection

# Import Blueprints from your routes folder
from routes.auth import auth_bp
from routes.catalog import catalog_bp
from routes.cart import cart_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = "my-secret-key-change-this"
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# 🔌 REGISTER THE BLUEPRINTS
app.register_blueprint(auth_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(cart_bp)

# Startup DB Checkers (from your old app.py)
def check_db_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    # Execute table generation logic directly using cur.execute()...
    conn.commit()
    conn.close()

# Force-reset debug link
@app.route("/d")
def clean_db_force():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS products; DROP TABLE IF EXISTS users;")
    conn.commit()
    conn.close()
    return redirect(url_for("catalog.index"))

# if __name__ == "__main__":
#     app.run(debug=True)

# new one to test with. 
if __name__ == "__main__":
    # Add host="0.0.0.0" inside app.run()
    app.run(host="0.0.0.0", debug=True)