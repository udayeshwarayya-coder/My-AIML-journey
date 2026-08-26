# Day 16 Practice — Inheritance
# Project 4: Library Management System (Part 4)
# Topic: Inheritance, super(), method overriding, isinstance()
# Goal: Build EBook class that inherits from Book, and load_mixed_catalog()

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================
# SETUP: Your complete Book class from Day 15 is below.
# Do NOT modify it. Read it, then write EBook below it.
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
        return f"[{self.book_id}] {self.title} — {self.author} | Rs.{self._price} | Genre: {self.genre} | {status}"

    def __repr__(self):
        return (f'Book(book_id="{self.book_id}", title="{self.title}", '
                f'author="{self.author}", price={self._price}, '
                f'genre="{self.genre}", available={self.available})')

    @classmethod
    def from_string(cls, data_string):
        data = data_string.strip().split(",")
        return cls(data[0], data[1], data[2], int(data[3]), data[4])

    @staticmethod
    def is_valid_price(price):
        return isinstance(price, (int, float)) and price > 0

    @staticmethod
    def genre_label(genre):
        labels = {
            "Programming":  "💻",
            "Self-Help":    "🌱",
            "Productivity": "⚡",
            "Fiction":      "📖",
        }
        return labels.get(genre, "📚")


# ============================================================
# TASK: Build the EBook class below
# ============================================================
# EBook is a child of Book. It has one extra attribute: download_link
#
# CSV format for EBook:
#   "E001,Clean Code,Robert Martin,499,Programming,http://books.com/cc"
#   (6 fields — same as Book + download_link at the end)
# ============================================================

class EBook(Book):
    def __init__(self, book_id, title, author, price, genre, download_link="No link found", available=True):
        super().__init__(book_id, title, author, price, genre, available)
        self.download_link = download_link
    

    # ----------------------------------------------------------
    # TASK A: __init__(self, book_id, title, author, price,
    #                  genre, download_link, available=True)
    # ----------------------------------------------------------
    # 1. Call super().__init__(...) with the Book fields first.
    # 2. Then set self.download_link = download_link
    

    # ----------------------------------------------------------
    # TASK B: __str__(self)
    # ----------------------------------------------------------
    # 1. Get the parent string: base = super().__str__()
    # 2. Return: f"{base} | Link: {self.download_link}"
    def __str__(self):
        # YOUR CODE HERE
        s=super().__str__()
        return f"{s}|Link:{self.download_link}"

    # ----------------------------------------------------------
    # TASK C: __repr__(self)
    # ----------------------------------------------------------
    # Return a full developer string like:
    #   EBook(book_id="E001", title="Clean Code", author="Robert Martin",
    #         price=499, genre="Programming", available=True,
    #         download_link="http://books.com/cc")
    def __repr__(self):
        return (f'EBook(book_id="{self.book_id}", title="{self.title}", '
                f'author="{self.author}", price={self._price}, '
                f'genre="{self.genre}", available={self.available}, '
                f'download_link="{self.download_link}")')

    # ----------------------------------------------------------
    # TASK D: @classmethod from_string(cls, data_string)
    # ----------------------------------------------------------
    # data_string has 6 fields:
    #   "E001,Clean Code,Robert Martin,499,Programming,http://books.com/cc"
    # Split, convert price to int, return cls(...)
    @classmethod
    def from_string(cls, data_string):
        # YOUR CODE HERE
        d = data_string.strip().split(",")
        return cls(d[0], d[1], d[2], int(d[3]), d[4], d[5])


# ============================================================
# TASK 2: load_mixed_catalog(book_rows, ebook_rows)
# ============================================================
# Given two lists of CSV strings, build ONE catalog dict.
# Use Book.from_string for book_rows and EBook.from_string for ebook_rows.
# Return: {book_id: <Book or EBook>, ...}
#
# Hint:
#   catalog = {}
#   for row in book_rows:
#       b = Book.from_string(row)
#       catalog[b.book_id] = b
#   for row in ebook_rows:
#       eb = EBook.from_string(row)
#       catalog[eb.book_id] = eb
#   return catalog

def load_mixed_catalog(book_rows, ebook_rows):
    # YOUR CODE HERE
    catalog={}
    for row in book_rows:
        b=Book.from_string(row)
        catalog[b.book_id]=b
    for row in ebook_rows:
        eb=EBook.from_string(row)
        catalog[eb.book_id]=eb
    return catalog


# ============================================================
# TEST YOUR CODE — run: python practice.py
# ============================================================

if __name__ == "__main__":

    # ── Test EBook creation directly ────────────────────────
    print("=== EBook direct creation ===")
    eb1 = EBook("E001", "Clean Code", "Robert Martin", 499, "Programming",
                "http://books.com/clean-code")
    print(eb1)
    # Expected:
    # [E001] Clean Code — Robert Martin | Rs.499 | Genre: Programming | Available | Link: http://books.com/clean-code

    # ── Test isinstance ──────────────────────────────────────
    print("\n=== isinstance checks ===")
    b1 = Book("B001", "Atomic Habits", "James Clear", 399, "Self-Help")
    print(isinstance(eb1, Book))    # True  — EBook IS a Book
    print(isinstance(eb1, EBook))   # True
    print(isinstance(b1,  EBook))   # False — a plain Book is NOT an EBook
    print(isinstance(b1,  Book))    # True

    # ── Test EBook.from_string ───────────────────────────────
    print("\n=== EBook.from_string ===")
    eb2 = EBook.from_string("E002,Atomic Habits,James Clear,299,Self-Help,http://books.com/atomic")
    print(eb2)
    # Expected:
    # [E002] Atomic Habits — James Clear | Rs.299 | Genre: Self-Help | Available | Link: http://books.com/atomic

    # ── Test repr ───────────────────────────────────────────
    print("\n=== repr ===")
    print(repr(eb1))
    # Expected (one line):
    # EBook(book_id="E001", title="Clean Code", author="Robert Martin", price=499, genre="Programming", available=True, download_link="http://books.com/clean-code")

    # ── Test inherited operators ─────────────────────────────
    print("\n=== inherited operators ===")
    print(eb1 == eb1)   # True  (same book_id)
    print(eb2 < eb1)    # True  (299 < 499)

    # ── Test inherited static methods ────────────────────────
    print("\n=== inherited static methods ===")
    print(EBook.is_valid_price(299))     # True
    print(EBook.genre_label("Self-Help"))  # 🌱

    # ── Test load_mixed_catalog ──────────────────────────────
    print("\n=== load_mixed_catalog ===")
    book_rows = [
        "B001,Atomic Habits,James Clear,399,Self-Help",
        "B002,Deep Work,Cal Newport,299,Productivity",
    ]
    ebook_rows = [
        "E001,Clean Code,Robert Martin,499,Programming,http://books.com/cc",
        "E002,The Pragmatic Programmer,David Thomas,599,Programming,http://books.com/pp",
    ]
    catalog = load_mixed_catalog(book_rows, ebook_rows)
    print(f"Total items: {len(catalog)}")   # 4
    for item in catalog.values():
        print(item)
    # Expected (order: B001, B002, E001, E002):
    # [B001] Atomic Habits — James Clear | Rs.399 | Genre: Self-Help | Available
    # [B002] Deep Work — Cal Newport | Rs.299 | Genre: Productivity | Available
    # [E001] Clean Code — Robert Martin | Rs.499 | Genre: Programming | Available | Link: http://books.com/cc
    # [E002] The Pragmatic Programmer — David Thomas | Rs.599 | Genre: Programming | Available | Link: http://books.com/pp

    # ── Bonus: sort mixed catalog by price ──────────────────
    print("\n=== Bonus: sorted by price ===")
    sorted_items = sorted(catalog.values())
    for item in sorted_items:
        print(item)
    # Expected (cheapest to most expensive):
    # [B002] Deep Work — Cal Newport | Rs.299 | ...
    # [B001] Atomic Habits — James Clear | Rs.399 | ...
    # [E001] Clean Code — Robert Martin | Rs.499 | ...
    # [E002] The Pragmatic Programmer — David Thomas | Rs.599 | ...
