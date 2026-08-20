# Day 9 Practice — Online Shopping Cart (Part 1)
# Topic: Polymorphism — same method name, different behaviour
# Goal: Write 3 logic functions for Project 3

# ============================================================
# SETUP — Product base class + child classes
# ============================================================
# Read concepts.md first (10 min), then come back here.
#
# The Product class is provided — study it carefully.
# You'll be building on top of this for Days 9-12.

class Product:
    total_products = 0                         # class variable — counts all products

    def __init__(self, name, product_id, price, category):
        self.name       = name
        self.product_id = product_id
        self.price      = price
        self.category   = category
        Product.total_products += 1

    def __str__(self):
        return f"{self.name} [{self.product_id}] — {self.category} | Rs.{self.price}"

    def __repr__(self):
        return f"Product(name={self.name!r}, product_id={self.product_id!r}, price={self.price})"

    def calculate_price(self):
        return self.price                      # base: no discount, no shipping

    def get_details(self):    #imporatnt in website methods
        return {
            "name":        self.name,
            "product_id":  self.product_id,
            "price":       self.price,
            "category":    self.category,
            "type":        type(self).__name__,
            "final_price": self.calculate_price()
        }


# ============================================================
# FUNCTION 1: Write DigitalProduct class
# ============================================================
# DigitalProduct inherits from Product.
# Extra attribute: discount_pct (int) — percentage discount, e.g. 20 means 20% off
#
# Override calculate_price():
#   final price = price - (price * discount_pct / 100)
#
# Override get_details():
#   call super().get_details(), then add "discount_pct" key
#
# Example:
#   d = DigitalProduct("Python eBook", "P002", 500, "Books", discount_pct=20)
#   d.calculate_price()  →  400.0    (500 - 20%)
#   d.get_details()      →  {..., "discount_pct": 20, "final_price": 400.0}
#
# Hint: same super().__init__() pattern as Day 5 Manager class

# Write your DigitalProduct class here:
class DigitalProduct(Product):
    # YOUR CODE HERE
    def __init__(self, name, product_id, price, category,discount_pct):
        super().__init__(name, product_id, price, category)
        self.discount_pct=discount_pct
    def calculate_price(self):
        final_price=self.price*(1-(self.discount_pct/100))
        return final_price
    def get_details(self):
        details=super().get_details()
        details["discount_pct"]=self.discount_pct
        return details


# ============================================================
# FUNCTION 2: Write PhysicalProduct class
# ============================================================
# PhysicalProduct inherits from Product.
# Extra attribute: shipping_cost (int/float) — added on top of price
#
# Override calculate_price():
#   final price = price + shipping_cost
#
# Override get_details():
#   call super().get_details(), then add "shipping_cost" key
#
# Example:
#   p = PhysicalProduct("Keyboard", "P003", 1500, "Electronics", shipping_cost=100)
#   p.calculate_price()  →  1600
#   p.get_details()      →  {..., "shipping_cost": 100, "final_price": 1600}

# Write your PhysicalProduct class here:
class PhysicalProduct(Product):
    # YOUR CODE HERE
    def __init__(self, name, product_id, price, category,shipping_cost):
        super().__init__(name, product_id, price, category)
        self.shipping_cost=shipping_cost
    def calculate_price(self):
        final_price=self.price+self.shipping_cost
        return final_price
    def get_details(self):
        details=super().get_details()
        details["shipping_cost"]=self.shipping_cost
        return details


# ============================================================
# FUNCTION 3: add_to_cart(cart, product, quantity)
# ============================================================
# Takes:
#   cart     — a dict (may be empty {})
#   product  — a Product / DigitalProduct / PhysicalProduct object
#   quantity — int, how many to add
#
# What it should do:
#   - If product already in cart → increase quantity
#   - If product not in cart → add new entry
#   - Each cart entry is a dict:
#       {
#           "product_id": product.product_id,
#           "name":       product.name,
#           "quantity":   quantity,
#           "unit_price": product.calculate_price(),   ← uses polymorphism!
#           "subtotal":   product.calculate_price() * quantity
#       }
#
# Returns: the updated cart dict (key = product_id)
#
# Example:
#   cart = {}
#   add_to_cart(cart, keyboard, 2)
#   # cart = {"P003": {"product_id": "P003", "name": "Keyboard", "quantity": 2,
#   #                   "unit_price": 1600, "subtotal": 3200}}
#
# HINT: cart[product.product_id] is your key

# Write your function here:
def add_to_cart(cart, product, quantity):
    # YOUR CODE HERE
    if product.product_id in cart:
        cart[product.product_id]["quantity"]+=quantity
    else:
        cart[product.product_id]={
        
       "product_id": product.product_id,
       "name":       product.name,
       "quantity":   quantity,
       "unit_price": product.calculate_price(),  
       "subtotal":   product.calculate_price() * quantity
   
    }
    

# ============================================================
# TEST YOUR CODE
# ============================================================

print("=" * 55)
print("SETUP — Creating products")
print("=" * 55)

p1 = Product("Notebook", "P001", 200, "Stationery")
p2 = DigitalProduct("Python eBook", "P002", 500, "Books", discount_pct=20)
p3 = PhysicalProduct("Keyboard", "P003", 1500, "Electronics", shipping_cost=100)

for p in [p1, p2, p3]:
    print(p)


print()
print("=" * 55)
print("TEST 1 — calculate_price() — Polymorphism in action")
print("=" * 55)

print(f"Notebook final price:     Rs.{p1.calculate_price()}")
# Expected: Rs.200

print(f"Python eBook final price: Rs.{p2.calculate_price()}")
# Expected: Rs.400.0   (500 - 20%)

print(f"Keyboard final price:     Rs.{p3.calculate_price()}")
# Expected: Rs.1600    (1500 + 100)


print()
print("=" * 55)
print("TEST 2 — get_details()")
print("=" * 55)

print(p2.get_details())
# Expected: {..., "discount_pct": 20, "final_price": 400.0, "type": "DigitalProduct"}

print(p3.get_details())
# Expected: {..., "shipping_cost": 100, "final_price": 1600, "type": "PhysicalProduct"}


print()
print("=" * 55)
print("TEST 3 — add_to_cart()")
print("=" * 55)

cart = {}
add_to_cart(cart, p1, 3)
add_to_cart(cart, p3, 2)
add_to_cart(cart, p1, 1)   # P001 already in cart — should increase qty to 4

for item in cart.values():
    print(item)

# Expected:
# P001 — Notebook:  qty=4, unit=200,  subtotal=800
# P003 — Keyboard:  qty=2, unit=1600, subtotal=3200


print()
print("=" * 55)
print("TEST 4 — isinstance() checks (polymorphism check)")
print("=" * 55)

for p in [p1, p2, p3]:
    print(f"{p.name}: isinstance Product? {isinstance(p, Product)}")
    # ALL should be True — child IS also a Product

print(isinstance(p2, DigitalProduct))   # True
print(isinstance(p2, PhysicalProduct))  # False

print(f"\nTotal products created: {Product.total_products}")  # Expected: 3


# ============================================================
# BONUS CHALLENGE (optional — ~10 min)
# ============================================================
# 1. Add a BundleProduct class:
#    - Has a list of products (bundle_items)
#    - calculate_price() = sum of each product's calculate_price() with 5% bundle discount
#    - Example: bundle of eBook(400) + Notebook(200) = 570 after 5% discount
class BundleProduct(Product):
    
    def calculate_price(bp):
        total=0
        for p in bp:
            total+=p.calculate_price()
        return total + total*(5/100)
    
        
       

# 2. Write a function get_cart_total(cart) that:
#    - Takes the cart dict you built above
#    - Returns the total of all subtotals
#    - Example: 800 + 3200 = 4000

# Write your bonus here:
def get_cart_total(cart):
    total=0
    for k,v in cart.values():
        total+=v["subtotal"]
    return total