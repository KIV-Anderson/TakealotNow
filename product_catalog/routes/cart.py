# routes/cart.py
from flask import Blueprint, render_template, session, jsonify
from db import get_db_connection

# Create the Cart Blueprint
cart_bp = Blueprint('cart', __name__)

# Reusable helper to count total items in the session cart
def get_cart_count():
    cart = session.get("cart", {})
    return sum(cart.values())

# ==========================================
# STANDARD ROUTE: VIEW CART PAGE
# ==========================================
@cart_bp.route("/cart")
def cart():
    cart_data = session.get("cart", {})
    conn = get_db_connection()
    cur = conn.cursor()

    cart_items = []
    total = 0

    for product_id, quantity in cart_data.items():
        # Querying SQL Server matching your table indices
        cur.execute("SELECT id, name, price, description, category, image FROM products WHERE id=?", (product_id,))
        product = cur.fetchone()

        if product:
            subtotal = product[2] * quantity  # product[2] is price
            total += subtotal
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })

    conn.close()
    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total,
        cart_count=get_cart_count()
    )

# ==========================================
# BACKGROUND API ENDPOINT: ADD ITEM
# ==========================================
@cart_bp.route("/api/add_to_cart/<int:product_id>")
def api_add_to_cart(product_id):
    cart = session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    session["cart"] = cart

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT price FROM products WHERE id=?", (product_id,))
    product = cur.fetchone()
    conn.close()

    price = product[0] if product else 0
    quantity = cart[product_id]
    subtotal = price * quantity

    # Recalculate whole cart total for the front-end display update
    cart_total = 0
    for pid, qty in cart.items():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT price FROM products WHERE id=?", (pid,))
        p = cur.fetchone()
        conn.close()
        if p:
            cart_total += p[0] * qty

    return jsonify({
        "success": True,
        "quantity": quantity,
        "subtotal": subtotal,
        "cart_total": cart_total,
        "cart_count": get_cart_count()
    })

# ==========================================
# BACKGROUND API ENDPOINT: REMOVE ITEM
# ==========================================
@cart_bp.route("/api/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1
        if cart[product_id] <= 0:
            del cart[product_id]

    session["cart"] = cart

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT price FROM products WHERE id=?", (product_id,))
    product = cur.fetchone()
    conn.close()

    price = product[0] if product else 0
    quantity = cart.get(product_id, 0)
    subtotal = price * quantity

    cart_total = 0
    for pid, qty in cart.items():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT price FROM products WHERE id=?", (pid,))
        p = cur.fetchone()
        conn.close()
        if p:
            cart_total += p[0] * qty

    return jsonify({
        "success": True,
        "quantity": quantity,
        "subtotal": subtotal,
        "cart_total": cart_total,
        "cart_count": get_cart_count()
    })