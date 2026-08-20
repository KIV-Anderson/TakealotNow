# routes/catalog.py
from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename
from db import get_db_connection
import os

catalog_bp = Blueprint('catalog', __name__)

# Helper cart count can go here or be imported
def get_cart_count():
    from flask import session
    cart = session.get("cart", {})
    return sum(cart.values())

@catalog_bp.route("/")
def index():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    conn = get_db_connection()
    cur = conn.cursor()
    sql = "SELECT id, name, price, description, category, image FROM products WHERE 1=1"
    params = []

    if search:
        sql += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    if category:
        sql += " AND category = ?"
        params.append(category)

    sql += " ORDER BY id DESC"
    cur.execute(sql, params)
    products = cur.fetchall()
    conn.close()

    categories = ["Electronics", "Clothing", "Home", "Beauty", "Sports", "Toys", "Books", "Other"]
    return render_template("index.html", products=products, search=search, 
                           selected_category=category, categories=categories, cart_count=get_cart_count())

@catalog_bp.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        category = request.form["category"]
        image = request.files.get("image")
        filename = None

        if image and image.filename:
            filename = secure_filename(image.filename)
            # Use current_app because 'app' isn't explicitly defined here
            image.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO products (name, price, description, category, image) VALUES (?, ?, ?, ?, ?)", 
                    (name, price, description, category, filename))
        conn.commit()
        conn.close()
        return redirect(url_for("catalog.index"))

    return render_template("add_product.html")

@catalog_bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)