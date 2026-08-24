# Day 14 Practice — Magic Methods: __len__, __eq__, __lt__
# Project 4: Library Management System (Part 2)
# Topic: Comparison and length dunder methods
# Goal: Write count_books(), compare_books(), sort_catalog()

# ============================================================
# SETUP: Copy your fixed Book class from Day 13 below.
# The catalog is still a dict: {"B001": <Book>, "B002": <Book>, ...}
# ============================================================


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

    # -------------------------------------------------------
    # TASK A: Add __eq__ to Book
    # -------------------------------------------------------
    # Two books are equal if they have the same book_id.
    # Return NotImplemented if `other` is not a Book.
    def __eq__(self, other):
        # YOUR CODE HERE
        if not isinstance(other,Book):
            return NotImplemented
        return self.book_id==other.book_id

    # -------------------------------------------------------
    # TASK B: Add __lt__ to Book
    # -------------------------------------------------------
    # A book is "less than" another based on its price.
    # Return NotImplemented if `other` is not a Book.
    def __lt__(self, other):
        # YOUR CODE HERE
        if not isinstance(other,Book):
            return NotImplemented
        return self._price<other._price

    def __str__(self):
        status = "Available" if self.available else "Issued"
        return f"[{self.book_id}] {self.title} — {self.author} | Rs.{self._price} | Genre: {self.genre} | {status}"

    def __repr__(self):
        return (f'Book(book_id="{self.book_id}", title="{self.title}", '
                f'author="{self.author}", price={self._price}, '
                f'genre="{self.genre}", available={self.available})')


# ============================================================
# TASK 1: count_books(catalog)
# ============================================================
# Given a catalog dict, return a dict with:
#   {
#       "total": <int>,
#       "available": <int>,
#       "issued": <int>
#   }
# Hint: loop over catalog.values() and check book.available

def count_books(catalog):
    # YOUR CODE HERE
    total=len(catalog)
    available_count=sum(1 for book in catalog.values() if book.available)
    issued_count=sum(1 for book in catalog.values() if not book.available)
    
    return {
        "total":total,
        "available":available_count,
        "issued":issued_count
    }


# ============================================================
# TASK 2: compare_books(book1, book2)
# ============================================================
# Compare two Book objects. Return a dict:
#   {
#       "same_book": True/False,       ← use == (__eq__)
#       "cheaper": <Book or None>,     ← use < (__lt__); None if equal price
#       "price_diff": <int>            ← abs difference in price
#   }
# Hint: use the == and < operators you just defined

def compare_books(book1, book2):
    # YOUR CODE HERE
    cheaper=book1 if book1<book2 else book2
    price_diff=book1.price-book2.price
    return {
        "same_book":book1==book2,
        "cheaper":cheaper,
        "price_diff":price_diff
    }


# ============================================================
# TASK 3: sort_catalog(catalog, key="price")
# ============================================================
# Sort the catalog and return a LIST of Book objects (not a dict).
# key can be: "price", "title", or "author"
# Default sort: ascending (cheapest first / A-Z)
#
# Hints:
#   - For "price": sorted(books) works because you defined __lt__
#   - For "title" and "author": use sorted(books, key=lambda b: b.title)
#   - If key is invalid, return the list unsorted

def sort_catalog(catalog, key="price"):
    # YOUR CODE HERE
    books=list(catalog.values())
    if key=="price":
        return sorted(books)
    elif key=="title":
        return sorted(books, key=lambda b: b.title)
    elif key=="author":
        return sorted(books, key=lambda b: b.author)    
    return books

# ============================================================
# TEST YOUR CODE — run: python practice.py
# ============================================================

if __name__ == "__main__":

    b1 = Book("B001", "Clean Code",              "Robert Martin", 699, "Programming")
    b2 = Book("B002", "Atomic Habits",           "James Clear",   399, "Self-Help", available=False)
    b3 = Book("B003", "The Pragmatic Programmer","David Thomas",  799, "Programming")
    b4 = Book("B004", "Deep Work",               "Cal Newport",   299, "Productivity")
    b5 = Book("B001", "Clean Code",              "Robert Martin", 699, "Programming")  # duplicate of b1

    catalog = {
        "B001": b1,
        "B002": b2,
        "B003": b3,
        "B004": b4,
    }

    # ── Test __eq__ ─────────────────────────────────────────
    print("=== __eq__ Tests ===")
    print(b1 == b5)          # True  (same book_id B001)
    print(b1 == b2)          # False (different book_id)
    print(b1 == "B001")      # False (not a Book)

    # ── Test __lt__ ─────────────────────────────────────────
    print("\n=== __lt__ Tests ===")
    print(b4 < b1)           # True  (299 < 699)
    print(b1 < b4)           # False (699 > 299)
    print(b1 < b5)           # False (699 == 699, not strictly less)

    # ── Test count_books ────────────────────────────────────
    print("\n=== count_books ===")
    counts = count_books(catalog)
    print(counts)
    # Expected: {"total": 4, "available": 3, "issued": 1}

    # ── Test compare_books ──────────────────────────────────
    print("\n=== compare_books ===")
    result = compare_books(b1, b2)
    print(result)
    # Expected: {"same_book": False, "cheaper": b2 (399), "price_diff": 300}

    result2 = compare_books(b1, b5)
    print(result2)
    # Expected: {"same_book": True, "cheaper": None, "price_diff": 0}

    # ── Test sort_catalog ───────────────────────────────────
    print("\n=== sort_catalog by price ===")
    by_price = sort_catalog(catalog, key="price")
    for book in by_price:
        print(book)
    # Expected order: Deep Work(299) → Atomic Habits(399) → Clean Code(699) → Pragmatic(799)

    print("\n=== sort_catalog by title ===")
    by_title = sort_catalog(catalog, key="title")
    for book in by_title:
        print(book)
    # Expected order: Atomic Habits → Clean Code → Deep Work → The Pragmatic Programmer

    print("\n=== sort_catalog by author ===")
    by_author = sort_catalog(catalog, key="author")
    for book in by_author:
        print(book)
    # Expected order: Cal Newport → David Thomas → James Clear → Robert Martin
