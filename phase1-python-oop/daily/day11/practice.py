# Day 11 Practice — Online Shopping Cart (Part 3)
# Topic: Cart Item State, Modifying Quantities, Removing Items & Checkout Receipt
# Goal: Write 3 logic functions for Project 3

import random
from datetime import datetime

# ============================================================
# REVISIT FROM DAYS 9 & 10 — Product Classes, Coupons & Cart
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
        return {"valid": False, "discount_info": None, "message": "Invalid coupon code"}
    cc = coupon_code.upper()
    if cc in COUPON_DB:
        if subtotal < COUPON_DB[cc]["min_spend"]:
            return {"valid": False, "discount_info": None, "message": f"Requires minimum spend of Rs.{COUPON_DB[cc]['min_spend']}"}
        else:
            return {"valid": True, "discount_info": COUPON_DB[cc], "message": "Coupon applied successfully!"}
    else:
        return {"valid": False, "discount_info": None, "message": "Invalid coupon code"}


def apply_discount(subtotal, coupon_info):
    if coupon_info is None:
        return 0.0
    if coupon_info["type"] == 'pct':
        discount = subtotal * (coupon_info["value"] / 100)
    elif coupon_info["type"] == 'flat':
        discount = coupon_info["value"]
    else:
        discount = 0.0
    return min(subtotal, discount)


def get_total(cart, coupon_code=None, tax_pct=5):
    subtotal = sum(item["subtotal"] for item in cart.values())
    if coupon_code:
        validation = validate_coupon(coupon_code, subtotal)
        if validation["valid"]:
            discount = apply_discount(subtotal, validation["discount_info"])
            coupon_msg = validation["message"]
        else:
            discount = 0.0
            coupon_msg = validation["message"]
    else:
        discount = 0.0
        coupon_msg = "No coupon applied"
    discounted_amount = subtotal - discount
    tax = discounted_amount * (tax_pct / 100)
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
        cart[product.product_id]["subtotal"] = (
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


# ============================================================
# FUNCTION 1: update_quantity(cart, product_id, new_quantity)
# ============================================================
# Takes:
#   cart         — dict of cart items
#   product_id   — string, e.g. "P001"
#   new_quantity — integer (e.g. 5, 0, -1)
#
# Logic:
#   1. If product_id not in cart:
#        return {"success": False, "message": "Product not found in cart"}
#   2. If new_quantity <= 0:
#        Delete the product_id from cart (using del or cart.pop)
#        return {"success": True, "message": "Item removed from cart (quantity 0)", "action": "removed"}
#   3. If new_quantity > 0:
#        Update cart[product_id]["quantity"] = new_quantity
#        Recalculate cart[product_id]["subtotal"] = new_quantity * cart[product_id]["unit_price"]
#        return {"success": True, "message": "Quantity updated successfully", "action": "updated"}

def update_quantity(cart, product_id, new_quantity):
    # YOUR CODE HERE
    if product_id not in cart:
        return {"success":False,"message":"Product not found in cart"}
    else:
        if new_quantity <=0:
            del cart[product_id]
            return {"success":True,"message":"Item removed from cart (product quantity =0)","action":"removed"}
        
        if new_quantity >0:
            cart[product_id]["quantity"] = new_quantity
            cart[product_id]["subtotal"]=new_quantity * cart[product_id]["unit_price"]
            return {"success": True, "message": "Quantity updated successfully", "action": "updated"}

# ============================================================
# FUNCTION 2: remove_item(cart, product_id)
# ============================================================
# Takes:
#   cart       — dict of cart items
#   product_id — string, e.g. "P001"
#
# Logic:
#   1. If product_id in cart:
#        removed_item = cart.pop(product_id)
#        return {"success": True, "message": f"{removed_item['name']} removed from cart", "removed_item": removed_item}
#   2. Else:
#        return {"success": False, "message": "Item not found in cart", "removed_item": None}

def remove_item(cart, product_id):
    # YOUR CODE HERE
    if product_id in cart:
        removed_item=cart.pop(product_id)
        return {"success":True,"message":f"{removed_item['name']} removed from cart","removed_item":removed_item}
    else:
        return {"success": False, "message": "Item not found in cart", "removed_item": None}


# ============================================================
# FUNCTION 3: checkout(cart, coupon_code=None, payment_method="card")
# ============================================================
# Takes:
#   cart           — dict of cart items
#   coupon_code    — optional string, e.g. "SAVE10" or None
#   payment_method — string, e.g. "card", "upi", "cod" (default: "card")
#
# Logic:
#   1. If cart is empty (len(cart) == 0):
#        return {"success": False, "message": "Cart is empty. Cannot checkout.", "receipt": None}
#   2. Calculate financial totals using get_total(cart, coupon_code)
#   3. Create a snapshot copy of the items currently in the cart
#   4. Generate a unique order_id: e.g. f"ORD-{random.randint(10000, 99999)}"
#   5. Construct the receipt dictionary:
#        {
#            "order_id":       order_id,
#            "timestamp":      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#            "items":          item_list_or_snapshot,
#            "payment_method": payment_method.upper(),
#            "payment_status": "PAID" if payment_method.lower() != "cod" else "PENDING",
#            "financials":     financial_totals_dict
#        }
#   6. Empty/clear the cart: cart.clear()
#   7. Return {"success": True, "message": "Order placed successfully!", "receipt": receipt}

def checkout(cart, coupon_code=None, payment_method="card"):
    # YOUR CODE HERE
    if len(cart)==0:
        return {"success":False,"message":"cart is empty, cannot checkout","receipt":None}
    else:
        financial_totals=get_total(cart,coupon_code)
        items_in_cart=[item['name'] for item in cart.values()]
        order_id=f"ORD-{random.randint(10000, 99999)}"
        receipt={
            "order_id":order_id,
            "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items":items_in_cart,
            "payment_method":payment_method,
            "payment_status":"PAID" if payment_method.lower() != "cod" else "PENDING",
            "financials":financial_totals
        }
        cart.clear()
        return {"success":True,"message":"Order placed successfully, come again","receipt":receipt}


# ============================================================
# TEST YOUR CODE
# ============================================================
if __name__ == "__main__":
    from copy import deepcopy

    print("=" * 60)
    print("SETUP — Cart Initial State")
    print("=" * 60)

    p1 = Product("Notebook", "P001", 200, "Stationery")
    p2 = DigitalProduct("Python eBook", "P002", 500, "Books", discount_pct=20) # 400
    p3 = PhysicalProduct("Keyboard", "P003", 1500, "Electronics", shipping_cost=100) # 1600

    test_cart = {}
    add_to_cart(test_cart, p1, 2)  # 2 * 200 = 400
    add_to_cart(test_cart, p2, 1)  # 1 * 400 = 400
    add_to_cart(test_cart, p3, 1)  # 1 * 1600 = 1600

    print("Initial Cart Items:")
    for k, v in test_cart.items():
        print(f"  {k}: {v['name']} | Qty: {v['quantity']} | Subtotal: Rs.{v['subtotal']}")

    print()
    print("=" * 60)
    print("TEST 1 — update_quantity()")
    print("=" * 60)

    # 1. Update quantity of P001 from 2 to 5 -> subtotal becomes 1000
    res1 = update_quantity(test_cart, "P001", 5)
    print("Update P001 to 5:", res1)
    print("P001 new subtotal:", test_cart["P001"]["subtotal"]) # Expected: 1000

    # 2. Update quantity to 0 -> should remove item
    res2 = update_quantity(test_cart, "P002", 0)
    print("Update P002 to 0:", res2)
    print("Is P002 still in cart?", "P002" in test_cart) # Expected: False

    # 3. Non-existent product
    res3 = update_quantity(test_cart, "P999", 2)
    print("Update non-existent P999:", res3) # Expected: success: False

    print()
    print("=" * 60)
    print("TEST 2 — remove_item()")
    print("=" * 60)

    # Remove P001
    res_rem = remove_item(test_cart, "P001")
    print("Remove P001:", res_rem)
    print("Remaining items in cart:", list(test_cart.keys())) # Expected: ['P003']

    # Remove already removed item
    res_rem_again = remove_item(test_cart, "P001")
    print("Remove P001 again:", res_rem_again) # Expected: success: False

    print()
    print("=" * 60)
    print("TEST 3 — checkout()")
    print("=" * 60)

    # Re-add items for a clean checkout test
    checkout_cart = {}
    add_to_cart(checkout_cart, p1, 2) # 400
    add_to_cart(checkout_cart, p2, 1) # 400
    # Total subtotal = 800

    print("Checkout with SAVE10 coupon & UPI payment:")
    checkout_res = checkout(checkout_cart, coupon_code="SAVE10", payment_method="upi")
    print("Checkout status:", checkout_res["success"])
    print("Order ID:", checkout_res["receipt"]["order_id"] if checkout_res["receipt"] else None)
    print("Payment Status:", checkout_res["receipt"]["payment_status"] if checkout_res["receipt"] else None)
    print("Final Amount:", checkout_res["receipt"]["financials"]["final_total"] if checkout_res["receipt"] else None)
    print("Cart items after checkout (should be empty):", len(checkout_cart))

    print("\nCheckout with empty cart:")
    empty_res = checkout(checkout_cart)
    print("Empty cart checkout status:", empty_res["success"]) # Expected: False
