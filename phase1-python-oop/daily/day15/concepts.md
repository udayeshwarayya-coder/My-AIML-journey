# Day 15 — `@classmethod` and `@staticmethod`
## Project 4: Library Management System (Part 3)

> **Revisits from Days 1–14:** `class`, `__init__`, `@property`, `__str__`, `__repr__`, `__eq__`, `__lt__`

---

## What You Already Know (Quick Recap)

So far every method you've written uses `self` — it operates on **one specific object**:
```python
book.display()      # self = that specific book object
book.price = 500    # self = that specific book object
```

**Today**: Two new kinds of methods that don't need a specific object:
- `@classmethod` — belongs to the **class itself**
- `@staticmethod` — a plain **helper function** that lives inside the class

---

## Concept 1: `@classmethod` — Alternative Constructors

A class method receives the **class** (`cls`) instead of an instance (`self`).

The most common use: **create objects in different ways** (alternative constructors).

```python
class Book:
    def __init__(self, book_id, title, author, price, genre):
        self.book_id = book_id
        self.title   = title
        self.author  = author
        self._price  = price
        self.genre   = genre

    @classmethod
    def from_string(cls, data_string):
        # data_string = "B001,Clean Code,Robert Martin,699,Programming"
        parts = data_string.split(",")
        return cls(parts[0], parts[1], parts[2], int(parts[3]), parts[4])
```

```python
# Normal way:
b1 = Book("B001", "Clean Code", "Robert Martin", 699, "Programming")

# Alternative constructor via classmethod:
b2 = Book.from_string("B002,Atomic Habits,James Clear,399,Self-Help")

print(b2.title)   # Atomic Habits
print(b2.price)   # 399
```

> **Key rule:** Use `cls(...)` inside a classmethod, never `Book(...)` directly.
> This way it works correctly even if someone subclasses your `Book`.

---

## Concept 2: `@staticmethod` — Utility / Helper Functions

A static method has **no `self` and no `cls`**.
It's just a regular function that lives inside the class for organization.

```python
class Book:
    ...

    @staticmethod
    def is_valid_price(price):
        return isinstance(price, (int, float)) and price > 0

    @staticmethod
    def genre_label(genre):
        labels = {
            "Programming": "💻",
            "Self-Help":   "🌱",
            "Productivity":"⚡",
        }
        return labels.get(genre, "📚")
```

```python
# Call on the class directly — no object needed:
print(Book.is_valid_price(499))       # True
print(Book.is_valid_price(-10))       # False
print(Book.genre_label("Self-Help"))  # 🌱
```

---

## Concept 3: `@classmethod` vs `@staticmethod` — When to Use Which

| | `@classmethod` | `@staticmethod` |
|:---|:---|:---|
| First parameter | `cls` (the class) | nothing extra |
| Can create objects? | Yes — `cls(...)` | No (no access to class) |
| Use case | Alternative constructors, factory methods | Utility / validation helpers |
| Example | `Book.from_string(...)` | `Book.is_valid_price(500)` |

> **Simple rule:**
> - Need to create an object? → `@classmethod`
> - Just a helper with no object needed? → `@staticmethod`

---

## Concept 4: Real Example — All Together

```python
class Book:
    def __init__(self, book_id, title, author, price, genre, available=True):
        self.book_id   = book_id
        self.title     = title
        self.author    = author
        self._price    = price
        self.genre     = genre
        self.available = available

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value > 0:
            self._price = value
        else:
            raise ValueError("Price must be greater than 0")

    @classmethod
    def from_string(cls, data_string):
        """Create a Book from a comma-separated string."""
        parts = data_string.strip().split(",")
        return cls(parts[0], parts[1], parts[2], int(parts[3]), parts[4])

    @staticmethod
    def is_valid_price(price):
        """Check if price is a positive number."""
        return isinstance(price, (int, float)) and price > 0

    @staticmethod
    def genre_label(genre):
        """Return an emoji label for a genre."""
        labels = {
            "Programming": "💻",
            "Self-Help":   "🌱",
            "Productivity":"⚡",
            "Fiction":     "📖",
        }
        return labels.get(genre, "📚")

    def __str__(self):
        status = "Available" if self.available else "Issued"
        label  = Book.genre_label(self.genre)
        return f"[{self.book_id}] {self.title} — {self.author} | Rs.{self._price} | {label} {self.genre} | {status}"

    def __repr__(self):
        return (f'Book(book_id="{self.book_id}", title="{self.title}", '
                f'author="{self.author}", price={self._price}, '
                f'genre="{self.genre}", available={self.available})')
```

```python
# Using classmethod
b1 = Book.from_string("B001,Clean Code,Robert Martin,699,Programming")
print(b1)
# [B001] Clean Code — Robert Martin | Rs.699 | 💻 Programming | Available

# Using staticmethod
print(Book.is_valid_price(399))    # True
print(Book.is_valid_price(0))      # False
print(Book.genre_label("Fiction")) # 📖
```

---

## What You Are Building Today

**3 tasks for the Library Management System:**

| Task | What it does |
|:-----|:-------------|
| `Book.from_string(data)` | `@classmethod` — create a Book from a CSV string |
| `Book.is_valid_price(price)` | `@staticmethod` — validate a price value |
| `load_catalog(data_list)` | Standalone function — use `from_string` to build a catalog from a list of strings |

---

## 10-Minute Read Check

You now understand:
- [ ] `@classmethod` receives `cls`, used to create objects differently
- [ ] `@staticmethod` has no `self`/`cls`, just a helper inside the class
- [ ] Use `cls(...)` inside a classmethod, not the class name directly
- [ ] `@classmethod` = factory/constructor | `@staticmethod` = validator/utility

**Now open `practice.py` and write the tasks!**
