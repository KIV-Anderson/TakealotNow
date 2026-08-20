# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
import pyodbc

# Create the Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                        (username, email, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for("auth.login")) # Note the 'auth.' prefix
        except pyodbc.IntegrityError: 
            return "User already exists"

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, password FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("catalog.index")) # Redirects to catalog blueprint

        return "Invalid email or password"

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("catalog.index"))