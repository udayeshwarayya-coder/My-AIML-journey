# Day 12 — Flask Intro & Connecting Your Python Logic to the Web
## Project 3: Online Shopping Cart — Web Edition (Part 1)

> **Revisits from Days 9–11:** `Product`, `DigitalProduct`, `PhysicalProduct`, `add_to_cart`, `update_quantity`, `remove_item`, `checkout`, `validate_coupon`, `get_total`

---

## What You Already Know (Quick Recap)

You have a fully working Python shopping cart engine:
- Product classes with polymorphic `calculate_price()`
- Cart dictionary with `add_to_cart`, `update_quantity`, `remove_item`
- Coupon validation and full financial breakdown via `get_total`
- Checkout with receipt generation

**Today**: You wrap that engine inside Flask so a real browser can talk to it.

---

## Concept 1: What is Flask?

Flask is a **micro web framework** for Python. It lets you turn your Python functions into **web endpoints** (URLs) that a browser or frontend can call.

```
Browser (HTML page)  ──→  Flask Route (app.py)  ──→  Your Python Logic
                     ←──  JSON Response          ←──
```

- **Route** = a URL path like `/add-to-cart` mapped to a Python function
- **Request** = data coming *in* from the browser (JSON body, form data)
- **Response** = data going *out* back to the browser (JSON dict)

---

## Concept 2: Flask App Skeleton

```python
from flask import Flask, request, jsonify

app = Flask(__name__)          # Create the Flask app

@app.route("/")                # Decorator maps URL "/" to this function
def home():
    return "Hello, World!"     # Return plain text

@app.route("/api/products", methods=["GET"])
def get_products():
    data = [{"name": "Notebook", "price": 200}]
    return jsonify(data)       # Return JSON — always use jsonify()

if __name__ == "__main__":
    app.run(debug=True)        # debug=True = auto-reload on save
```

### Key decorators & functions

| Tool | What it does |
|:---|:---|
| `@app.route("/path")` | Maps a URL to a function |
| `methods=["GET","POST"]` | Allowed HTTP methods for that route |
| `request.get_json()` | Read JSON body sent by browser |
| `request.args.get("key")` | Read URL query params `?key=val` |
| `jsonify(dict)` | Convert Python dict → JSON response |

---

## Concept 3: HTTP Methods — GET vs POST

| Method | When to use | Example |
|:---|:---|:---|
| `GET` | Fetch / read data | Get product list, view cart |
| `POST` | Send / create data | Add to cart, apply coupon |
| `DELETE` | Remove data | Remove item from cart |
| `PUT` | Update data | Change item quantity |

```python
@app.route("/api/cart/add", methods=["POST"])
def add_item():
    data = request.get_json()      # {"product_id": "P001", "quantity": 2}
    product_id = data["product_id"]
    quantity   = data["quantity"]
    # ... call your add_to_cart() function here
    return jsonify({"success": True})
```

---

## Concept 4: Flask + Frontend Integration Flow

```
index.html (button click)
    -> fetch("/api/cart/add", { method: "POST", body: JSON })
        -> Flask route function runs
            -> Calls your Python cart logic
                -> Returns jsonify({...})
    -> JavaScript reads the response
        -> Updates the HTML page
```

You don't need to know JavaScript deeply — just understand this pattern:
1. HTML button click -> JavaScript calls a Flask URL
2. Flask function runs your Python logic
3. Flask returns JSON
4. JavaScript updates the page

---

## Concept 5: In-Memory State in Flask

Flask handles one request at a time. For today's project, you'll store the cart as a **module-level global dictionary** (in-memory state):

```python
# Global cart — lives as long as the server is running
cart = {}

@app.route("/api/cart/add", methods=["POST"])
def add_item():
    global cart
    data = request.get_json()
    # ... modify cart ...
    return jsonify(cart)
```

> In-memory means cart resets when the server restarts. That's fine for now — databases come later.

---

## What You're Building Today

**Day 12 Routes for the Shopping Cart Web App:**

| Route | Method | What it does |
|:---|:---|:---|
| `GET /` | GET | Serve the HTML page |
| `GET /api/products` | GET | Return the products catalogue |
| `POST /api/cart/add` | POST | Add a product to the cart |
| `GET /api/cart` | GET | Return current cart contents |
| `PUT /api/cart/update` | PUT | Change quantity of a cart item |
| `DELETE /api/cart/remove` | DELETE | Remove an item from the cart |
| `POST /api/cart/checkout` | POST | Checkout, generate receipt |

---

## 10-Minute Read Check

You now understand:
- [ ] What Flask does and why it bridges Python to browser
- [ ] How `@app.route` maps a URL to a Python function
- [ ] When to use GET vs POST vs DELETE vs PUT
- [ ] How `request.get_json()` reads browser data
- [ ] How `jsonify()` sends Python dicts back as JSON
- [ ] How in-memory cart state works in Flask

**Now open `practice.py` and build the Flask app!**
