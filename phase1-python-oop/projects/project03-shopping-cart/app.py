# ============================================================
# app.py — Online Shopping Cart (Flask Web App)
# ============================================================
# HOW THIS FILE WORKS:
#   1. Flask reads this file and registers every @app.route
#   2. When a browser hits a URL, Flask calls the matching function
#   3. The function runs your Python cart logic
#   4. jsonify() converts the Python dict to JSON and sends it back
#
# HOW TO RUN:
#   pip install flask
#   python app.py
#   Open http://localhost:5000 in your browser
# ============================================================

from flask import Flask, request, jsonify, send_from_directory
import random
from datetime import datetime
import os

# Flask(__name__) creates the app.
# __name__ tells Flask where to look for templates/ and static/ folders.
app = Flask(__name__)

# ============================================================
# CART ENGINE — Your logic from Days 9-11
# ============================================================

class Product:
    def __init__(self, name, product_id, price, category):
        self.name       = name
        self.product_id = product_id
        self._price     = price
        self.category   = category

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self._price = new_price

    def calculate_price(self):
        return self._price

    def get_details(self):
        return {
            "name":        self.name,
            "product_id":  self.product_id,
            "price":       self.price,
            "category":    self.category,
            "type":        type(self).__name__,   # Returns "Product", "DigitalProduct" etc.
            "final_price": self.calculate_price()
        }


class DigitalProduct(Product):
    def __init__(self, name, product_id, price, category, discount_pct=0):
        super().__init__(name, product_id, price, category)
        self.discount_pct = discount_pct

    def calculate_price(self):
        return self.price * (1 - self.discount_pct / 100)

    def get_details(self):
        details = super().get_details()
        details["discount_pct"] = self.discount_pct
        return details


class PhysicalProduct(Product):
    def __init__(self, name, product_id, price, category, shipping_cost=0):
        super().__init__(name, product_id, price, category)
        self.shipping_cost = shipping_cost

    def calculate_price(self):
        return self.price + self.shipping_cost

    def get_details(self):
        details = super().get_details()
        details["shipping_cost"] = self.shipping_cost
        return details


# ============================================================
# COUPON & PRICING FUNCTIONS
# ============================================================

COUPON_DB = {
    "SAVE10":  {"type": "pct",  "value": 10,  "min_spend": 500},
    "FLAT100": {"type": "flat", "value": 100, "min_spend": 1000},
    "WELCOME": {"type": "pct",  "value": 20,  "min_spend": 0},
}


def validate_coupon(coupon_code, subtotal):
    if not coupon_code:
        return {"valid": False, "discount_info": None, "message": "No coupon applied"}
    cc = coupon_code.upper()
    if cc in COUPON_DB:
        if subtotal < COUPON_DB[cc]["min_spend"]:
            return {"valid": False, "discount_info": None,
                    "message": f"Requires minimum spend of Rs.{COUPON_DB[cc]['min_spend']}"}
        return {"valid": True, "discount_info": COUPON_DB[cc], "message": "Coupon applied successfully!"}
    return {"valid": False, "discount_info": None, "message": "Invalid coupon code"}


def apply_discount(subtotal, coupon_info):
    if coupon_info is None:
        return 0.0
    if coupon_info["type"] == "pct":
        discount = subtotal * (coupon_info["value"] / 100)
    elif coupon_info["type"] == "flat":
        discount = coupon_info["value"]
    else:
        discount = 0.0
    return min(subtotal, discount)


def get_total(cart, coupon_code=None, tax_pct=5):
    subtotal = sum(item["subtotal"] for item in cart.values())
    if coupon_code:
        validation = validate_coupon(coupon_code, subtotal)
        discount   = apply_discount(subtotal, validation["discount_info"]) if validation["valid"] else 0.0
        coupon_msg = validation["message"]
    else:
        discount   = 0.0
        coupon_msg = "No coupon applied"
    discounted_amount = subtotal - discount
    tax         = discounted_amount * (tax_pct / 100)
    final_total = discounted_amount + tax
    return {
        "subtotal":       round(subtotal, 2),
        "discount":       round(discount, 2),
        "discounted_amt": round(discounted_amount, 2),
        "tax":            round(tax, 2),
        "final_total":    round(final_total, 2),
        "coupon_message": coupon_msg
    }


def add_to_cart(cart, product, quantity):
    if product.product_id in cart:
        cart[product.product_id]["quantity"] += quantity
        cart[product.product_id]["subtotal"]  = (
            cart[product.product_id]["quantity"] * cart[product.product_id]["unit_price"]
        )
    else:
        cart[product.product_id] = {
            "product_id": product.product_id,
            "name":       product.name,
            "quantity":   quantity,
            "unit_price": product.calculate_price(),
            "subtotal":   product.calculate_price() * quantity
        }
    return cart


def update_quantity(cart, product_id, new_quantity):
    if product_id not in cart:
        return {"success": False, "message": "Product not found in cart"}
    if new_quantity <= 0:
        del cart[product_id]
        return {"success": True, "message": "Item removed from cart", "action": "removed"}
    cart[product_id]["quantity"] = new_quantity
    cart[product_id]["subtotal"] = new_quantity * cart[product_id]["unit_price"]
    return {"success": True, "message": "Quantity updated successfully", "action": "updated"}


def remove_item(cart, product_id):
    if product_id in cart:
        removed_item = cart.pop(product_id)
        return {"success": True, "message": f"{removed_item['name']} removed from cart", "removed_item": removed_item}
    return {"success": False, "message": "Item not found in cart", "removed_item": None}


# ============================================================
# PRODUCT CATALOGUE — In-memory product database
# ============================================================

PRODUCTS_DB = {
    "P001": Product("Notebook",       "P001",  200, "Stationery"),
    "P002": DigitalProduct("Python eBook",    "P002",  500, "Books",        discount_pct=20),
    "P003": PhysicalProduct("Keyboard",       "P003", 1500, "Electronics",  shipping_cost=100),
    "P004": PhysicalProduct("Mouse",          "P004",  800, "Electronics",  shipping_cost=50),
    "P005": DigitalProduct("DSA Course",      "P005", 1200, "Courses",      discount_pct=15),
    "P006": Product("Pen Set",        "P006",   80, "Stationery"),
}

# ============================================================
# IN-MEMORY CART — Shared across all requests this session
# ============================================================
# NOTE: This resets every time you restart the server.
#       A real app would use a database (SQLite, PostgreSQL, etc.)
cart = {}


# ============================================================
# ROUTE 1: Serve HTML Frontend
# GET /
# ============================================================
# send_from_directory(folder, filename) reads a file from disk and
# sends it to the browser as an HTTP response.
# "templates" is the folder name relative to this file.

@app.route("/")
def home():
    return send_from_directory("templates", "index.html")
    # Flask reads  templates/index.html  and sends it to the browser


# ============================================================
# ROUTE 2: Get All Products
# GET /api/products
# ============================================================
# The browser calls this to populate the product catalogue cards.
# We loop through PRODUCTS_DB and call .get_details() on each product.

@app.route("/api/products", methods=["GET"])
def get_products():
    # Build a list of product detail dicts
    products_list = [product.get_details() for product in PRODUCTS_DB.values()]
    # jsonify() converts the Python list → JSON response
    return jsonify(products_list)


# ============================================================
# ROUTE 3: Add Item to Cart
# POST /api/cart/add
# Body (JSON): {"product_id": "P001", "quantity": 1}
# ============================================================
# request.get_json() reads the JSON body the browser sent.
# We validate the product exists, then call add_to_cart().

@app.route("/api/cart/add", methods=["POST"])
def add_item():
    # Read the JSON body the browser sent
    # Force=True means accept even if Content-Type header is missing
    data = request.get_json(force=True)

    product_id = data.get("product_id")
    quantity   = int(data.get("quantity", 1))

    # Validate the product exists in our catalogue
    if product_id not in PRODUCTS_DB:
        # Return a 404 error response — browser sees {"success": False, "message": "..."}
        return jsonify({"success": False, "message": "Product not found"}), 404

    # Call your Day 11 cart engine function
    add_to_cart(cart, PRODUCTS_DB[product_id], quantity)

    # Return success + updated cart info
    return jsonify({
        "success":    True,
        "message":    "Item added to cart",
        "cart":       list(cart.values()),
        "cart_count": len(cart)
    })


# ============================================================
# ROUTE 4: Get Cart Contents
# GET /api/cart
# Optional query param: ?coupon=SAVE10
# ============================================================
# request.args.get("key") reads URL query parameters like /api/cart?coupon=SAVE10

@app.route("/api/cart", methods=["GET"])
def get_cart():
    # Get optional coupon from query string (e.g. /api/cart?coupon=SAVE10)
    coupon_code = request.args.get("coupon", None)

    # Calculate financial breakdown using the cart engine
    totals = get_total(cart, coupon_code)

    return jsonify({
        "items":      list(cart.values()),   # All items in the cart
        "cart_count": len(cart),
        "financials": totals                 # subtotal, discount, tax, final_total
    })


# ============================================================
# ROUTE 5: Update Item Quantity
# PUT /api/cart/update
# Body (JSON): {"product_id": "P001", "quantity": 3}
# ============================================================
# PUT is used for updates (changing existing data).

@app.route("/api/cart/update", methods=["PUT"])
def update_item():
    data = request.get_json(force=True)

    product_id   = data.get("product_id")
    new_quantity = int(data.get("quantity", 1))

    # Call your Day 11 update function
    result = update_quantity(cart, product_id, new_quantity)

    return jsonify({
        "result":     result,
        "cart":       list(cart.values()),
        "cart_count": len(cart)
    })


# ============================================================
# ROUTE 6: Remove Item from Cart
# DELETE /api/cart/remove
# Body (JSON): {"product_id": "P001"}
# ============================================================
# DELETE is used when you're removing a resource entirely.

@app.route("/api/cart/remove", methods=["DELETE"])
def remove_from_cart():
    data = request.get_json(force=True)

    product_id = data.get("product_id")

    # Call your Day 11 remove function
    result = remove_item(cart, product_id)

    return jsonify({
        "result":     result,
        "cart":       list(cart.values()),
        "cart_count": len(cart)
    })


# ============================================================
# ROUTE 7: Checkout — Generate Order Receipt
# POST /api/cart/checkout
# Body (JSON): {"coupon_code": "SAVE10", "payment_method": "upi"}
# ============================================================
# POST because we're creating a new order (resource creation).

@app.route("/api/cart/checkout", methods=["POST"])
def checkout_order():
    # .get_json() with silent=True returns None if body is missing
    data = request.get_json(silent=True) or {}

    coupon_code    = data.get("coupon_code", None)
    payment_method = data.get("payment_method", "card")

    # Can't checkout an empty cart
    if len(cart) == 0:
        return jsonify({"success": False, "message": "Cart is empty. Cannot checkout."}), 400

    # Calculate financials using your Day 11 engine
    financials = get_total(cart, coupon_code)

    # Snapshot — capture item names before clearing cart
    items_snapshot = [item["name"] for item in cart.values()]

    # Generate a unique order ID
    order_id = f"ORD-{random.randint(10000, 99999)}"

    # Build the receipt
    receipt = {
        "order_id":       order_id,
        "timestamp":      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items":          items_snapshot,
        "payment_method": payment_method.upper(),
        # "PAID" for card/upi, "PENDING" for Cash on Delivery
        "payment_status": "PAID" if payment_method.lower() != "cod" else "PENDING",
        "financials":     financials
    }

    # Clear the cart — order is placed
    cart.clear()

    return jsonify({
        "success": True,
        "message": "Order placed successfully!",
        "receipt": receipt
    })


# ============================================================
# RUN THE SERVER
# ============================================================
# debug=True  → auto-reloads when you save this file (dev only)
# port=5000   → open http://localhost:5000 in browser

if __name__ == "__main__":
    app.run(debug=True, port=5000)
