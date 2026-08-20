# Day 10 — Encapsulation
## Project 3: Online Shopping Cart

> **Revisits from Day 9:** `Product`, `DigitalProduct`, `PhysicalProduct`, polymorphism, `calculate_price()`, `add_to_cart()`

---

## What You Already Know (Quick Recap)

On Day 9, you built products and an `add_to_cart()` function:

```python
cart = {}
add_to_cart(cart, p1, 3)
```

Right now, anyone can directly do:
```python
cart["P001"]["unit_price"] = 0        # 🚨 Customer changed price to 0!
cart["P001"]["subtotal"] = -500       # 🚨 Negative subtotal!
```

In a real shopping application, **direct manipulation of internal data causes huge bugs and security holes**.  
Today we fix this using **Encapsulation**.

---

## What is Encapsulation?

**Encapsulation** means:
1. **Bundling data and methods** together inside a class.
2. **Restricting direct access** to internal variables from outside the class.
3. Providing controlled entry points (methods) to read or update that data safely.

Think of an ATM: you don't directly open the cash vault and grab money; you interact through the keypad (a controlled method).

---

## Public vs Protected vs Private in Python

Python uses naming conventions for access levels:

| Level | Syntax | Meaning / Convention | Can access from outside? |
|:---|:---|:---|:---:|
| **Public** | `self.name` | Open to everyone | ✅ Yes |
| **Protected** | `self._discount` | Internal use for class & subclasses | ⚠️ Yes (by convention, "do not touch") |
| **Private** | `self.__secret_code` | Strictly internal to this class only | ❌ No (Python renames it via *Name Mangling*) |

---

## How Private Variables (`__var`) Work

When you prefix an attribute with double underscores `__`, Python automatically performs **Name Mangling**:

```python
class CouponManager:
    def __init__(self):
        self.__secret_key = "STORE_2026"   # Private attribute

manager = CouponManager()

# print(manager.__secret_key)
# 💥 AttributeError: 'CouponManager' object has no attribute '__secret_key'

# Python secretly renamed it to _ClassName__attribute:
print(manager._CouponManager__secret_key)   # "STORE_2026" (accessible but discourages direct use)
```

---

## Today's Architecture — Encapsulating the Cart & Coupons

```
Coupon Rules (Encapsulated)
├── "SAVE10"  → 10% off (min spend Rs.500)
├── "FLAT100" → Rs.100 off (min spend Rs.1000)
└── "WELCOME" → 20% off (no min spend)

ShoppingCart (Class with private state)
├── __items       (dict of cart items — no external tampering)
├── __discount    (applied discount amount)
├── add_item()    (controlled addition)
├── apply_coupon()(validates & sets discount)
└── get_total()   (computes subtotal, discount, tax, final total)
```

---

## The Pattern

```python
class ShoppingCart:
    # Encapsulated coupon database (private to the class)
    __COUPONS = {
        "SAVE10":  {"type": "pct",  "value": 10,  "min_spend": 500},
        "FLAT100": {"type": "flat", "value": 100, "min_spend": 1000},
        "WELCOME": {"type": "pct",  "value": 20,  "min_spend": 0},
    }

    def __init__(self):
        self.__items = {}          # Private: outside code cannot corrupt this dict
        self.__applied_coupon = None

    def _validate_coupon(self, code, subtotal):
        """Protected helper method: verifies code and minimum spend."""
        if code not in self.__COUPONS:
            return {"valid": False, "message": "Invalid coupon code"}
        
        coupon = self.__COUPONS[code]
        if subtotal < coupon["min_spend"]:
            return {
                "valid": False,
                "message": f"Coupon requires minimum spend of Rs.{coupon['min_spend']}"
            }
        
        return {"valid": True, "coupon": coupon, "message": "Coupon applied successfully"}
```

---

## What You're Building Today

**Day 10 Logic Functions for Project 3:**

| Function / Method | What it does |
|:---|:---|
| `validate_coupon(coupon_code, subtotal)` | Checks coupon validity against encapsulated rules & min spend |
| `apply_discount(subtotal, coupon_info)` | Calculates discount amount based on `pct` or `flat` type |
| `get_total(cart, coupon_code=None)` | Returns complete cart summary (`subtotal`, `discount`, `tax`, `final_total`) |

---

## Common Mistakes to Avoid

| Mistake | Fix |
|:---|:---|
| Allowing discount to exceed subtotal | Always ensure `discount <= subtotal` so total never goes negative (`max(0, total)`) |
| Accessing `__items` directly from outside | Use getter methods (e.g. `get_items()` or methods inside the class) |
| Hardcoding coupon values across multiple places | Keep coupon data encapsulated in one lookup dictionary |
| Forgetting percentage calculation | `pct` discount is `subtotal * (value / 100)`, not `subtotal - value` |

---

## 10-Minute Read Check ✅

You now understand:
- [ ] Why direct variable access is dangerous in production apps
- [ ] Difference between `name` (public), `_name` (protected), and `__name` (private)
- [ ] How Python name mangling works (`_ClassName__var`)
- [ ] How to encapsulate coupon validation logic and cart totals

**Now open `practice.py` and write your 3 functions!**
