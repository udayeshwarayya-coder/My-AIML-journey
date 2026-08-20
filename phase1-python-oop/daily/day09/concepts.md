# Day 9 — Polymorphism
## Project 3: Online Shopping Cart

> **Revisits from Day 5-8:** Classes, `__init__`, `super()`, inheritance, method overriding

---

## What You Already Know (Quick Recap)

```python
class Employee:
    def calculate_pay(self):
        return self.base_salary       # base version

class Manager(Employee):
    def calculate_pay(self):          # OVERRIDE — Manager's own version
        return self.base_salary + self.team_size * 5000
```

You already did this in Days 5-8 — that IS polymorphism.  
Today you name it properly and practice it with a new example.

---

## What is Polymorphism?

**Poly** = many | **morphism** = forms  
Same method name, different behaviour depending on which class calls it.

```python
emp = Employee("Uday", "E001", 50000)
mgr = Manager("Arjun", "M001", 80000, team_size=5)

emp.calculate_pay   # → 50000           (Employee's version)
mgr.calculate_pay   # → 80000 + 25000   (Manager's version)
```

Same name `calculate_pay` → different result → **polymorphism**.

---

## How It Works in Python

Python checks the *actual type* of the object at runtime:

```python
for worker in [emp, mgr, intern]:
    print(worker.calculate_pay)   # calls the RIGHT version each time
```

This is why you can loop through a list of mixed types and it "just works."

---

## Today's Example — Product Types

```
Product (base)
├── price = 500
└── calculate_price() → 500          (just return price)

DigitalProduct(Product)
├── price = 500
├── discount_pct = 10
└── calculate_price() → 450          (price - 10% discount)

PhysicalProduct(Product)
├── price = 500
├── shipping_cost = 50
└── calculate_price() → 550          (price + shipping)
```

All three have `calculate_price()`.  
Each returns something different.  
That is polymorphism.

---

## The Pattern

```python
class Product:
    def __init__(self, name, product_id, price, category):
        self.name       = name
        self.product_id = product_id
        self.price      = price
        self.category   = category

    def calculate_price(self):
        return self.price              # base: just the price

    def get_details(self):
        return {
            "name":       self.name,
            "product_id": self.product_id,
            "price":      self.price,
            "category":   self.category,
            "type":       type(self).__name__,
            "final_price": self.calculate_price()
        }


class DigitalProduct(Product):
    def __init__(self, name, product_id, price, category, discount_pct=0):
        super().__init__(name, product_id, price, category)
        self.discount_pct = discount_pct

    def calculate_price(self):              # OVERRIDE
        return self.price * (1 - self.discount_pct / 100)


class PhysicalProduct(Product):
    def __init__(self, name, product_id, price, category, shipping_cost=0):
        super().__init__(name, product_id, price, category)
        self.shipping_cost = shipping_cost

    def calculate_price(self):              # OVERRIDE
        return self.price + self.shipping_cost
```

---

## Key Point — `super().__init__()` Again

Same rule as Day 5:

```python
class DigitalProduct(Product):
    def __init__(self, name, product_id, price, category, discount_pct=0):
        super().__init__(name, product_id, price, category)  # ← always first
        self.discount_pct = discount_pct                      # ← then own extras
```

Without `super().__init__()`, `self.name`, `self.price` etc. won't exist.

---

## Polymorphism in Action

```python
products = [
    Product("Notebook", "P001", 200, "Stationery"),
    DigitalProduct("Python eBook", "P002", 500, "Books", discount_pct=20),
    PhysicalProduct("Keyboard", "P003", 1500, "Electronics", shipping_cost=100),
]

for p in products:
    print(f"{p.name}: Rs.{p.calculate_price()}")

# Output:
# Notebook:     Rs.200
# Python eBook: Rs.400.0    (500 - 20%)
# Keyboard:     Rs.1600     (1500 + 100)
```

---

## What You're Building Today

**Online Shopping Cart — Day 9 Functions:**

| What | What it does |
|------|-------------|
| `Product` base class | Blueprint with `name`, `product_id`, `price`, `category` |
| `add_to_cart(cart, product, quantity)` | Adds a product to the cart dict |
| `calculate_price(product)` | Calls `product.calculate_price()` — polymorphism in action |

Today you write **pure logic** — no Flask, no website yet. That comes on Day 12.

---

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Forgetting `super().__init__()` in child | Always call it before adding your own attributes |
| Calling `calculate_price()` instead of `calculate_price` | It's a regular method today (no `@property` yet — that's Day 11) |
| Mixing up `price` (original) vs `calculate_price()` (final) | `price` = what you set. `calculate_price()` = what customer pays |
| Using `type(p) == 'DigitalProduct'` to check type | Use `isinstance(p, DigitalProduct)` instead |

---

## 10-Minute Read Check ✅

You now understand:
- [ ] What polymorphism means (same method, different behaviour)
- [ ] How Python picks the right method at runtime
- [ ] How to override a parent method in a child class
- [ ] Why `super().__init__()` is still needed
- [ ] The Product / DigitalProduct / PhysicalProduct pattern

**Now open `practice.py` and write your 3 functions!**
