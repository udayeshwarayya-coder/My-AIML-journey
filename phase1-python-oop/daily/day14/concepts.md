# Day 14 — Magic Methods: `__len__`, `__eq__`, `__lt__`
## Project 4: Library Management System (Part 2)

> **Revisits from Days 1–13:** `class`, `__init__`, `@property`, `__str__`, `__repr__`

---

## What You Already Know (Quick Recap)

Yesterday you built `__str__` and `__repr__` to control how a `Book` **looks**.

**Today**: Three more magic methods that let your objects **behave** like built-in Python types — so you can use `len()`, `==`, and `<` directly on them.

---

## Concept 1: `__len__` — Make `len()` Work on Your Object

`__len__` controls what `len(object)` returns.

```python
class Library:
    def __init__(self):
        self.catalog = {}

    def add_book(self, book):
        self.catalog[book.book_id] = book

    def __len__(self):
        return len(self.catalog)   # number of books in library


lib = Library()
lib.add_book(book1)
lib.add_book(book2)

print(len(lib))   # 2  ← calls __len__ automatically
```

**Without `__len__`:**
```python
len(lib)   # TypeError: object of type 'Library' has no len()
```

**Rule:** `__len__` must return an **integer ≥ 0**.

---

## Concept 2: `__eq__` — Make `==` Work on Your Objects

`__eq__` controls what `object1 == object2` means.

By default, `==` checks if two variables point to the **same object in memory**.
With `__eq__`, you define what "equal" means logically.

```python
class Book:
    def __init__(self, book_id, title, author, price, genre):
        self.book_id = book_id
        self.title   = title
        self.author  = author
        self._price  = price
        self.genre   = genre

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented          # don't compare with non-Book objects
        return self.book_id == other.book_id   # two books are equal if same ID
```

```python
b1 = Book("B001", "Clean Code", "Robert Martin", 699, "Programming")
b2 = Book("B001", "Clean Code", "Robert Martin", 699, "Programming")  # same ID
b3 = Book("B002", "Atomic Habits", "James Clear", 399, "Self-Help")

print(b1 == b2)   # True   ← same book_id
print(b1 == b3)   # False  ← different book_id
print(b1 == "B001")  # NotImplemented → Python falls back → False
```

> **Why return `NotImplemented`?**
> It tells Python: "I don't know how to compare with this type — try the other side."
> Never `raise` an error here; return `NotImplemented` instead.

---

## Concept 3: `__lt__` — Make `<` Work (Enable Sorting!)

`__lt__` controls `object1 < object2`.

The magic power: **once you define `__lt__`, Python's `sorted()` and `list.sort()` work automatically on your objects!**

```python
class Book:
    ...
    def __lt__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self._price < other._price   # sort books by price
```

```python
b1 = Book("B001", "Clean Code", "Robert Martin", 699, "Programming")
b2 = Book("B002", "Atomic Habits", "James Clear", 399, "Self-Help")
b3 = Book("B003", "Deep Work", "Cal Newport", 299, "Productivity")

print(b3 < b1)   # True  (299 < 699)

books = [b1, b2, b3]
sorted_books = sorted(books)          # sorted by price — uses __lt__
for b in sorted_books:
    print(b)
# Deep Work — Rs.299
# Atomic Habits — Rs.399
# Clean Code — Rs.699
```

---

## Concept 4: Comparison Methods — Full Table

| Magic Method | Operator | Meaning |
|:-------------|:---------|:--------|
| `__eq__(self, other)` | `==` | Equal |
| `__ne__(self, other)` | `!=` | Not equal (Python auto-generates from `__eq__` if missing) |
| `__lt__(self, other)` | `<`  | Less than |
| `__le__(self, other)` | `<=` | Less than or equal |
| `__gt__(self, other)` | `>`  | Greater than |
| `__ge__(self, other)` | `>=` | Greater than or equal |

> **Shortcut:** Define `__eq__` + `__lt__` → use `@functools.total_ordering` to auto-generate the rest. But for now, just `__eq__` and `__lt__` are enough.

---

## Concept 5: Real Example — All Three Together

```python
class Library:
    def __init__(self, name):
        self.name    = name
        self.catalog = {}   # {book_id: Book}

    def add_book(self, book):
        self.catalog[book.book_id] = book

    def __len__(self):
        return len(self.catalog)

    def __str__(self):
        return f"Library '{self.name}' — {len(self)} books"


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

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self.book_id == other.book_id

    def __lt__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self._price < other._price

    def __str__(self):
        status = "Available" if self.available else "Issued"
        return f"[{self.book_id}] {self.title} — {self.author} | Rs.{self._price} | {self.genre} | {status}"

    def __repr__(self):
        return (f'Book(book_id="{self.book_id}", title="{self.title}", '
                f'author="{self.author}", price={self._price}, '
                f'genre="{self.genre}", available={self.available})')
```

---

## What You Are Building Today

**3 logic functions for the Library Management System:**

| Function | What it does |
|:---------|:-------------|
| `count_books(catalog)` | Uses `__len__`-style logic: returns total, available, and issued counts |
| `compare_books(book1, book2)` | Uses `__eq__` and `__lt__` to compare two books and return a summary |
| `sort_catalog(catalog, key)` | Sorts the catalog by `"price"`, `"title"`, or `"author"` using `sorted()` |

---

## 10-Minute Read Check

You now understand:
- [ ] `__len__`  → makes `len(obj)` work, must return an int
- [ ] `__eq__`   → defines what `==` means for your objects
- [ ] `__lt__`   → defines `<`, which enables `sorted()` on your objects
- [ ] Always return `NotImplemented` (not raise) when type doesn't match
- [ ] One `__lt__` is all you need to make a list of objects sortable

**Now open `practice.py` and write the 3 functions!**
