# Day 12 Practice — Flask Web App for Online Shopping Cart
# Topic: Flask Routing, HTTP Methods, Frontend-Backend Integration
# Goal: Write 7 Flask route functions that expose your cart engine to the browser

from flask import Flask, request, jsonify, send_from_directory
import random
from datetime import datetime
import os

app = Flask(__name__)

# ============================================================
# CART ENGINE — Your logic from Days 9-11 (already written for you)
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
            "type":        type(self).__name__,
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


COUPON_DB = {
    "SAVE10":  {"type": "pct",  "value": 10,  "min_spend": 500},
    "FLAT100": {"type": "flat", "value": 100, "min_spend": 1000},
    "WELCOME": {"type": "pct",  "value": 20,  "min_spend": 0},
}


def validate_coupon(coupon_code, subtotal):
    if not coupon_code:
        return {"valid": False, "discount_info": None, "message": "No coupon provided"}
    cc = coupon_code.upper()
    if cc in COUPON_DB:
        if subtotal < COUPON_DB[cc]["min_spend"]:
            return {"valid": False, "discount_info": None, "message": f"Requires min spend of Rs.{COUPON_DB[cc]['min_spend']}"}
        return {"valid": True, "discount_info": COUPON_DB[cc], "message": "Coupon applied!"}
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
        return {"success": True, "message": "Item removed from cart (quantity 0)", "action": "removed"}
    cart[product_id]["quantity"] = new_quantity
    cart[product_id]["subtotal"] = new_quantity * cart[product_id]["unit_price"]
    return {"success": True, "message": "Quantity updated successfully", "action": "updated"}


def remove_item(cart, product_id):
    if product_id in cart:
        removed_item = cart.pop(product_id)
        return {"success": True, "message": f"{removed_item['name']} removed from cart", "removed_item": removed_item}
    return {"success": False, "message": "Item not found in cart", "removed_item": None}


# ============================================================
# PRODUCT CATALOGUE — In-memory database (lookup by product_id)
# ============================================================

PRODUCTS_DB = {
    "P001": Product("Notebook",      "P001",  200,  "Stationery"),
    "P002": DigitalProduct("Python eBook",   "P002",  500,  "Books",       discount_pct=20),
    "P003": PhysicalProduct("Keyboard",      "P003", 1500,  "Electronics", shipping_cost=100),
    "P004": PhysicalProduct("Mouse",         "P004",  800,  "Electronics", shipping_cost=50),
    "P005": DigitalProduct("DSA Course",     "P005", 1200,  "Courses",     discount_pct=15),
    "P006": Product("Pen Set",       "P006",   80,  "Stationery"),
}

# ============================================================
# IN-MEMORY CART — Shared state for this server session
# ============================================================

cart = {}

# ============================================================
# ROUTE 1: Serve HTML frontend
# ============================================================
# Method: GET
# URL: /
# Logic: Use send_from_directory to serve index.html from the
#        "templates" folder (same folder as this file)
# Return: The HTML file

@app.route("/")
def home():
    # YOUR CODE HERE
    pass


# ============================================================
# ROUTE 2: GET /api/products
# ============================================================
# Method: GET
# URL: /api/products
# Logic:
#   1. Loop through PRODUCTS_DB
#   2. Call .get_details() on each product
#   3. Return jsonify(list of all product detail dicts)

@app.route("/api/products", methods=["GET"])
def get_products():
    # YOUR CODE HERE
    pass


# ============================================================
# ROUTE 3: POST /api/cart/add
# ============================================================
# Method: POST
# URL: /api/cart/add
# Receives JSON body: {"product_id": "P001", "quantity": 2}
# Logic:
#   1. Read JSON body using request.get_json()
#   2. Get product_id and quantity from body
#   3. If product_id not in PRODUCTS_DB:
#        return jsonify({"success": False, "message": "Product not found"}), 404
#   4. Call add_to_cart(cart, PRODUCTS_DB[product_id], quantity)
#   5. Return jsonify({"success": True, "cart": cart, "cart_count": len(cart)})

@app.route("/api/cart/add", methods=["POST"])
def add_item():
    # YOUR CODE HERE
    pass


# ============================================================
# ROUTE 4: GET /api/cart
# ============================================================
# Method: GET
# URL: /api/cart
# Logic:
#   1. Get financial totals using get_total(cart)
#   2. Return jsonify({
#          "items": list(cart.values()),
#          "cart_count": len(cart),
#          "financials": totals
#      })

@app.route("/api/cart", methods=["GET"])
def get_cart():
    # YOUR CODE HERE
    pass


# ============================================================
# ROUTE 5: PUT /api/cart/update
# ============================================================
# Method: PUT
# URL: /api/cart/update
# Receives JSON body: {"product_id": "P001", "quantity": 5}
# Logic:
#   1. Read JSON body
#   2. Call update_quantity(cart, product_id, quantity)
#   3. Return jsonify({"result": result, "cart": list(cart.values()), "cart_count": len(cart)})

@app.route("/api/cart/update", methods=["PUT"])
def update_item():
    # YOUR CODE HERE
    pass


# ============================================================
# ROUTE 6: DELETE /api/cart/remove
# ============================================================
# Method: DELETE
# URL: /api/cart/remove
# Receives JSON body: {"product_id": "P001"}
# Logic:
#   1. Read JSON body
#   2. Call remove_item(cart, product_id)
#   3. Return jsonify({"result": result, "cart": list(cart.values()), "cart_count": len(cart)})

@app.route("/api/cart/remove", methods=["DELETE"])
def remove_from_cart():
    # YOUR CODE HERE
    pass


# ============================================================
# ROUTE 7: POST /api/cart/checkout
# ============================================================
# Method: POST
# URL: /api/cart/checkout
# Receives JSON body: {"coupon_code": "SAVE10", "payment_method": "upi"}
#   (both are optional — default coupon=None, payment_method="card")
# Logic:
#   1. Read JSON body (use {} as fallback if no body sent)
#   2. Get coupon_code and payment_method from body
#   3. If cart is empty:
#        return jsonify({"success": False, "message": "Cart is empty"}), 400
#   4. Calculate financials using get_total(cart, coupon_code)
#   5. Generate order_id = f"ORD-{random.randint(10000, 99999)}"
#   6. Build receipt dict (same structure as Day 11)
#   7. cart.clear()
#   8. Return jsonify({"success": True, "receipt": receipt})

@app.route("/api/cart/checkout", methods=["POST"])
def checkout_order():
    # YOUR CODE HERE
    pass


# ============================================================
# RUN THE SERVER
# ============================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
