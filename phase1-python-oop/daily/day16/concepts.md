# Day 16 — Inheritance
## Project 4: Library Management System (Part 4)

> **Revisits from Days 1–15:** `class`, `__init__`, `@property`, `__str__`, `__repr__`, `__eq__`, `__lt__`, `@classmethod`, `@staticmethod`

---

## What You Already Know (Quick Recap)

You have a solid `Book` class. Every method so far lives in one class and every object is of type `Book`.

**Today**: What if you want a *special kind* of book — like an `EBook` that also has a `download_link`, or a `PhysicalBook` that tracks `shelf_location`?

You **don't rewrite** `Book` from scratch. You **inherit** from it.

---

## Concept 1: Inheritance — "Is-a" Relationship

A **child class** inherits all attributes and methods of its **parent class**.

```python
class EBook(Book):   # EBook inherits from Book
    pass
```

Now `EBook` automatically has `book_id`, `title`, `author`, `price`, `genre`, `available`, `__str__`, `__repr__`, `__eq__`, `__lt__`, `from_string`, `is_valid_price`, `genre_label` — everything from `Book`.

```python
eb = EBook("E001", "Clean Code", "Robert Martin", 499, "Programming")
print(eb.title)     # Clean Code  (inherited)
print(eb.price)     # 499         (inherited)
print(eb)           # works via inherited __str__
```

---

## Concept 2: Extending `__init__` with `super()`

The child class needs its own extra attributes. Use `super().__init__()` to call the parent's `__init__` first, then add your own.

```python
class EBook(Book):
    def __init__(self, book_id, title, author, price, genre,
                 download_link, available=True):
        super().__init__(book_id, title, author, price, genre, available)
        self.download_link = download_link   # EBook-only attribute
```

> **Rule:** Always call `super().__init__(...)` as the **first line** inside the child's `__init__`.

---

## Concept 3: Overriding Methods

The child can **replace** any parent method by defining it with the same name.

```python
class EBook(Book):
    def __init__(self, book_id, title, author, price, genre,
                 download_link, available=True):
        super().__init__(book_id, title, author, price, genre, available)
        self.download_link = download_link

    def __str__(self):          # overrides Book.__str__
        base = super().__str__()   # reuse parent string
        return f"{base} | Link: {self.download_link}"
```

```python
eb = EBook("E001", "Clean Code", "Robert Martin", 499, "Programming",
           "http://books.com/clean-code")
print(eb)
# [E001] Clean Code — Robert Martin | Rs.499 | Genre: Programming | Available | Link: http://books.com/clean-code
```

---

## Concept 4: `isinstance()` — Check the Type

```python
b  = Book("B001", "Atomic Habits", "James Clear", 399, "Self-Help")
eb = EBook("E001", "Clean Code", "Robert Martin", 499, "Programming", "http://...")

isinstance(b,  Book)    # True
isinstance(eb, Book)    # True  <- EBook IS a Book!
isinstance(eb, EBook)   # True
isinstance(b,  EBook)   # False <- a plain Book is NOT an EBook
```

> This is the **"is-a" relationship**: an `EBook` *is a* `Book`, so it passes all `isinstance(x, Book)` checks.

---

## Concept 5: `@classmethod` `from_string` in the Child

Because you used `cls(...)` in `Book.from_string`, it already works on subclasses for fields the parent knows. For `EBook`, which needs `download_link`, you override `from_string`:

```python
class EBook(Book):
    ...
    @classmethod
    def from_string(cls, data_string):
        # format: "E001,Clean Code,Robert Martin,499,Programming,http://books.com/cc"
        parts = data_string.strip().split(",")
        return cls(parts[0], parts[1], parts[2], int(parts[3]), parts[4], parts[5])
```

---

## Concept 6: Real Example — All Together

```python
class EBook(Book):
    def __init__(self, book_id, title, author, price, genre,
                 download_link, available=True):
        super().__init__(book_id, title, author, price, genre, available)
        self.download_link = download_link

    def __str__(self):
        base = super().__str__()
        return f"{base} | Link: {self.download_link}"

    def __repr__(self):
        return (f'EBook(book_id="{self.book_id}", title="{self.title}", '
                f'author="{self.author}", price={self._price}, '
                f'genre="{self.genre}", available={self.available}, '
                f'download_link="{self.download_link}")')

    @classmethod
    def from_string(cls, data_string):
        parts = data_string.strip().split(",")
        return cls(parts[0], parts[1], parts[2], int(parts[3]), parts[4], parts[5])
```

---

## What You Are Building Today

| Task | What it does |
|:-----|:-------------|
| `EBook.__init__` | Inherit from `Book`, add `download_link` |
| `EBook.__str__` | Extend parent `__str__` with download link |
| `EBook.__repr__` | Full developer repr for EBook |
| `EBook.from_string` | Override classmethod to parse 6-field CSV |
| `load_mixed_catalog` | Build a catalog from both Book and EBook CSV rows |

---

## 10-Minute Read Check

You now understand:
- [ ] A child class inherits all methods and attributes from the parent
- [ ] `super().__init__(...)` calls the parent constructor
- [ ] Overriding a method replaces it in the child class
- [ ] `super().method()` lets you reuse the parent version inside an override
- [ ] `isinstance(obj, Book)` returns `True` for both `Book` and `EBook` objects

**Now open `practice.py` and write the tasks!**
