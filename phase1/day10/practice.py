# Day 10 Practice — Online Shopping Cart (Part 2)
# Topic: Encapsulation — Data Protection, Private Variables & Coupon Logic
# Goal: Write 3 logic functions for Project 3

# ============================================================
# REVISIT FROM DAY 9 — Product Classes & Setup
# ============================================================

class Product:
    def __init__(self, name, product_id, price, category):
        self.name       = name
        self.product_id = product_id
        self.price      = price
        self.category   = category

    def calculate_price(self):
        return self.price

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


# ============================================================
# COUPON DATABASE (Encapsulated Rules)
# ============================================================
# Available coupons:
# "SAVE10"  -> 10% off (min_spend: 500)
# "FLAT100" -> Flat Rs.100 off (min_spend: 1000)
# "WELCOME" -> 20% off (min_spend: 0)

COUPON_DB = {
    "SAVE10":  {"type": "pct",  "value": 10,  "min_spend": 500},
    "FLAT100": {"type": "flat", "value": 100, "min_spend": 1000},
    "WELCOME": {"type": "pct",  "value": 20,  "min_spend": 0},
}


# ============================================================
# FUNCTION 1: validate_coupon(coupon_code, subtotal)
# ============================================================
# Takes:
#   coupon_code — string (e.g. "SAVE10", "INVALID")
#   subtotal    — float/int, current cart subtotal
#
# Logic:
#   1. Convert coupon_code to uppercase (case-insensitive)
#   2. If coupon_code not in COUPON_DB:
#        return {"valid": False, "discount_info": None, "message": "Invalid coupon code"}
#   3. If subtotal < coupon's min_spend:
#        return {"valid": False, "discount_info": None, "message": f"Requires minimum spend of Rs.{min_spend}"}
#   4. Otherwise:
#        return {"valid": True, "discount_info": coupon_dict, "message": "Coupon applied successfully!"}

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


# ============================================================
# FUNCTION 2: apply_discount(subtotal, coupon_info)
# ============================================================
# Takes:
#   subtotal    — float/int
#   coupon_info — dict from COUPON_DB (e.g. {"type": "pct", "value": 10, "min_spend": 500})
#                 or None if no coupon is applied
#
# Logic:
#   1. If coupon_info is None:
#        return 0.0
#   2. If coupon_info["type"] == "pct":
#        discount = subtotal * (coupon_info["value"] / 100)
#   3. If coupon_info["type"] == "flat":
#        discount = coupon_info["value"]
#   4. Ensure discount never exceeds subtotal: return min(discount, subtotal)

def apply_discount(subtotal, coupon_info):
    # YOUR CODE HERE
    if coupon_info==None:
        return 0.0
    else:
        if coupon_info["type"]=='pct':
            discount= subtotal*(coupon_info["value"]/100)
        elif coupon_info["type"]=='flat':
            discount=(coupon_info["value"])
        else:
            discount=0
        return min(subtotal,discount)


# ============================================================
# FUNCTION 3: get_total(cart, coupon_code=None, tax_pct=5)
# ============================================================
# Takes:
#   cart        — dict of items (from Day 9 add_to_cart)
#                 Example: {"P001": {"quantity": 2, "unit_price": 200, "subtotal": 400}}
#   coupon_code — optional string (e.g. "SAVE10" or None)
#   tax_pct     — float/int, default 5 (meaning 5% GST/tax on discounted amount)
#
# Logic:
#   1. Calculate subtotal = sum of all item["subtotal"] in cart
#   2. If coupon_code is provided:
#        validation = validate_coupon(coupon_code, subtotal)
#        if validation["valid"]:
#            discount = apply_discount(subtotal, validation["discount_info"])
#            coupon_msg = validation["message"]
#        else:
#            discount = 0.0
#            coupon_msg = validation["message"]
#      Else:
#        discount = 0.0
#        coupon_msg = "No coupon applied"
#   3. discounted_amount = subtotal - discount
#   4. tax = discounted_amount * (tax_pct / 100)
#   5. final_total = discounted_amount + tax
#
# Returns dict:
#   {
#       "subtotal":        subtotal,
#       "discount":        round(discount, 2),
#       "discounted_amt":  round(discounted_amount, 2),
#       "tax":             round(tax, 2),
#       "final_total":     round(final_total, 2),
#       "coupon_message":  coupon_msg
#   }

def get_total(cart, coupon_code=None, tax_pct=5):
    # YOUR CODE HERE
    subtotal=0
    for p in cart.keys():
        subtotal+=cart[p]["subtotal"]
    if coupon_code:
        validation=validate_coupon(coupon_code,subtotal)
        if validation["valid"]:
            discount=apply_discount(subtotal,validation["discount_info"])
            coupon_msg = validation["message"]
        else:
            discount=0
            coupon_msg=validation["message"]
    else:
        discount=0
        coupon_msg="no coupon appllied"
    discounted_amount=subtotal-discount
    tax=discounted_amount*(tax_pct/100)
    final_total=discounted_amount + tax
    return {
        "subtotal":subtotal,
        "discount":round(discount,2),
        "discounted_amt":round(discounted_amount,2),
        "tax":round(tax,2),
        "final_total":round(final_total,2),
        "coupon_message":  coupon_msg
    }


# ============================================================
# TEST YOUR CODE
# ============================================================
if __name__ == "__main__":
    from copy import deepcopy

    print("=" * 60)
    print("SETUP — Cart Sample Data")
    print("=" * 60)

    cart = {
        "P001": {"product_id": "P001", "name": "Notebook", "quantity": 2, "unit_price": 200, "subtotal": 400},
        "P002": {"product_id": "P002", "name": "Python eBook", "quantity": 1, "unit_price": 400.0, "subtotal": 400.0},
    }
    # Current Cart Subtotal = 800.0

    print()
    print("=" * 60)
    print("TEST 1 — validate_coupon()")
    print("=" * 60)

    print("SAVE10 on 800:", validate_coupon("SAVE10", 800))
    # Expected: {'valid': True, 'discount_info': {'type': 'pct', 'value': 10, 'min_spend': 500}, 'message': 'Coupon applied successfully!'}

    print("FLAT100 on 800 (min spend 1000):", validate_coupon("FLAT100", 800))
    # Expected: {'valid': False, 'discount_info': None, 'message': 'Requires minimum spend of Rs.1000'}

    print("FAKECODE on 800:", validate_coupon("FAKECODE", 800))
    # Expected: {'valid': False, 'discount_info': None, 'message': 'Invalid coupon code'}


    print()
    print("=" * 60)
    print("TEST 2 — apply_discount()")
    print("=" * 60)

    c_pct = COUPON_DB["SAVE10"]
    c_flat = COUPON_DB["FLAT100"]

    print("10% on 800:", apply_discount(800, c_pct))
    # Expected: 80.0

    print("Flat 100 on 1200:", apply_discount(1200, c_flat))
    # Expected: 100

    print("No coupon (None):", apply_discount(800, None))
    # Expected: 0.0


    print()
    print("=" * 60)
    print("TEST 3 — get_total()")
    print("=" * 60)

    # 1. No coupon: Subtotal 800, Tax 5% (40) -> Total 840
    print("Without coupon:")
    print(get_total(cart))

    # 2. SAVE10 coupon: Subtotal 800, Disc 10% (80), Tax 5% on 720 (36) -> Total 756
    print("\nWith SAVE10 coupon:")
    print(get_total(cart, coupon_code="SAVE10"))

    # 3. Invalid min-spend coupon FLAT100: No discount applied
    print("\nWith FLAT100 (below min spend):")
    print(get_total(cart, coupon_code="FLAT100"))


    # ============================================================
    # BONUS CHALLENGE (optional — Encapsulated ShoppingCart Class)
    # ============================================================
    # Create a ShoppingCart class that hides its __items dict as private:
    # class ShoppingCart:
    #     def __init__(self):
    #         self.__items = {}
    #         self.__applied_coupon = None
    #
    #     def add_item(self, product, quantity): ...
    #     def apply_coupon(self, code): ...
    #     def get_summary(self): ...
