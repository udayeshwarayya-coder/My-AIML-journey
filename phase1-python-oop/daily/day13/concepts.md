# Day 13 — Magic Methods: `__str__` and `__repr__`
## Project 4: Library Management System (Part 1)

> **Revisits from Days 1–12:** `class`, `__init__`, `self`, `@property`, Inheritance, Encapsulation

---

## What You Already Know (Quick Recap)

You've been using `get_details()` to return a dict from your objects:
```python
product.get_details()  # returns {"name": "Notebook", "price": 200, ...}
```

**Today**: Python has *built-in* magic methods that let you control how your objects
look when printed or logged — no `.get_details()` needed.

---

## Concept 1: What Are Magic Methods?

Magic methods (also called **dunder methods** — double underscore) are special
Python methods with `__` before and after the name.

You already know one:
```python
def __init__(self, ...):   # Called automatically when you create an object
```

Today you learn two more:
```python
def __str__(self):    # Called when you print() an object
def __repr__(self):   # Called in the console / for debugging
```

---

## Concept 2: `__str__` — Human-Friendly String

`__str__` controls what `print(object)` shows.
Think of it as: *"What should a human reader see?"*

```python
class Book:
    def __init__(self, title, author, price):
        self.title  = title
        self.author = author
        self.price  = price

    def __str__(self):
        return f'"{self.title}" by {self.author} — Rs.{self.price}'


b = Book("Python Crash Course", "Eric Matthes", 499)

print(b)        # "Python Crash Course" by Eric Matthes — Rs.499
print(str(b))   # same as above — str() calls __str__
```

**Without `__str__`:**
```python
print(b)   # <__main__.Book object at 0x000001A3B>   <- useless!
```

---

## Concept 3: `__repr__` — Developer-Friendly String

`__repr__` controls what the console shows, and is used for debugging.
Think of it as: *"How do I recreate this object exactly?"*

```python
class Book:
    def __init__(self, title, author, price, book_id):
        self.title   = title
        self.author  = author
        self.price   = price
        self.book_id = book_id

    def __repr__(self):
        return f'Book(book_id="{self.book_id}", title="{self.title}", author="{self.author}", price={self.price})'
```

```python
b = Book("Python Crash Course", "Eric Matthes", 499, "B001")

repr(b)
# Book(book_id="B001", title="Python Crash Course", author="Eric Matthes", price=499)

# In a list, Python uses __repr__ automatically:
books = [b]
print(books)
#[Book(book_id="B001", title="Python Crash Course", author="Eric Matthes", price=499)]
```

---

## Concept 4: `__str__` vs `__repr__` — When Does Each Fire?

| Situation | Which method called |
|:----------|:--------------------|
| `print(obj)` | `__str__` (falls back to `__repr__` if missing) |
| `str(obj)` | `__str__` |
| `repr(obj)` | `__repr__` |
| `f"{obj}"` in f-string | `__str__` |
| Printing a list of objects | `__repr__` for each item |
| Python console / REPL | `__repr__` |

**Golden Rule:**
- `__str__`  → for **users** — readable, pretty
- `__repr__` → for **developers** — exact, reconstructable

---

## Concept 5: Real Example — Both Together

```python
class Book:
    def __init__(self, title, author, price, book_id, genre, available=True):
        self.book_id   = book_id
        self.title     = title
        self.author    = author
        self._price    = price
        self.genre     = genre
        self.available = available

    @property
    def price(self):
        return self._price

    def __str__(self):
        status = "Available" if self.available else "Issued"
        return f"[{self.book_id}] {self.title} — {self.author} | Rs.{self.price} | {status}"

    def __repr__(self):
        return (f'Book(book_id="{self.book_id}", title="{self.title}", '
                f'author="{self.author}", price={self.price}, '
                f'genre="{self.genre}", available={self.available})')


b1 = Book("Clean Code", "Robert Martin", 699, "B001", "Programming")
b2 = Book("Atomic Habits", "James Clear", 399, "B002", "Self-Help", available=False)

print(b1)   # [B001] Clean Code — Robert Martin | Rs.699 | Available
print(b2)   # [B002] Atomic Habits — James Clear | Rs.399 | Issued

library = [b1, b2]
print(library)
# [Book(book_id="B001", ...), Book(book_id="B002", ...)]
```

---

## What You Are Building Today

**3 logic functions for the Library Management System:**

| Function | What it does |
|:---------|:-------------|
| `Book` class with `__str__` and `__repr__` | Represents one library book |
| `add_book(catalog, book)` | Adds a book to the library catalog dict |
| `display_catalog(catalog)` | Prints all books in the catalog neatly |

---

## 10-Minute Read Check

You now understand:
- [ ] What magic/dunder methods are
- [ ] `__str__` = human-friendly (fires on `print()`)
- [ ] `__repr__` = developer-friendly (fires in console, lists)
- [ ] When each one is called automatically by Python
- [ ] Why they replace the need for `.get_details()` in many cases

**Now open `practice.py` and write the 3 functions!**
