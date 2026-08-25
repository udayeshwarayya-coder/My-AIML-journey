# Day 15 Practice — @classmethod and @staticmethod
# Project 4: Library Management System (Part 3)
# Topic: Class methods and static methods
# Goal: Add from_string(), is_valid_price(), genre_label(), and load_catalog()

# ============================================================
# SETUP: Copy your fixed Book class from Day 14 below.
# The catalog is still a dict: {"B001": <Book>, "B002": <Book>, ...}
# ============================================================


import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

    # -------------------------------------------------------
    # TASK A: Add @classmethod  from_string(cls, data_string)
    # -------------------------------------------------------
    # data_string format: "B001,Clean Code,Robert Martin,699,Programming"
    # Split by comma, convert price to int, return a new Book object.
    # Use cls(...) — NOT Book(...) directly.
    @classmethod
    def from_string(cls, data_string):
        # YOUR CODE HERE
        data=data_string.strip().split(",")
        return cls(data[0],data[1],data[2],int(data[3]),data[4])
    

    # -------------------------------------------------------
    # TASK B: Add @staticmethod  is_valid_price(price)
    # -------------------------------------------------------
    # Return True if price is a positive int or float, False otherwise.
    # Hint: use isinstance(price, (int, float)) and price > 0
    @staticmethod
    def is_valid_price(price):
        # YOUR CODE HERE
        return isinstance(price,(int,float)) and price >0

    # -------------------------------------------------------
    # TASK C: Add @staticmethod  genre_label(genre)
    # -------------------------------------------------------
    # Return an emoji string for the genre.
    # Mapping:
    #   "Programming"  → "💻"
    #   "Self-Help"    → "🌱"
    #   "Productivity" → "⚡"
    #   "Fiction"      → "📖"
    #   anything else  → "📚"
    @staticmethod
    def genre_label(genre):
        # YOUR CODE HERE
        labels={
        "Programming" : "💻",
       "Self-Help"    : "🌱",
       "Productivity" : "⚡",
       "Fiction"      : "📖"
               }
        return labels.get(genre,"📚")

# ============================================================
# TASK 1: load_catalog(data_list)
# ============================================================
# Given a list of CSV strings, build and return a catalog dict.
# Each string: "B001,Clean Code,Robert Martin,699,Programming"
# Use Book.from_string() inside this function.
# Return: {"B001": <Book>, "B002": <Book>, ...}
#
# Hint:
#   catalog = {}
#   for row in data_list:
#       book = Book.from_string(row)
#       catalog[book.book_id] = book
#   return catalog

def load_catalog(data_list):
    # YOUR CODE HERE
    catalog={}
    for d in data_list:
        b=Book.from_string(d)
        catalog[b.book_id]=b
    return catalog


# ============================================================
# TEST YOUR CODE — run: python practice.py
# ============================================================

if __name__ == "__main__":

    # ── Test is_valid_price ──────────────────────────────────
    print("=== is_valid_price ===")
    print(Book.is_valid_price(499))     # True
    print(Book.is_valid_price(0))       # False
    print(Book.is_valid_price(-50))     # False
    print(Book.is_valid_price("free"))  # False

    # ── Test genre_label ────────────────────────────────────
    print("\n=== genre_label ===")
    print(Book.genre_label("Programming"))   # 💻
    print(Book.genre_label("Self-Help"))     # 🌱
    print(Book.genre_label("Productivity"))  # ⚡
    print(Book.genre_label("Fiction"))       # 📖
    print(Book.genre_label("History"))       # 📚

    # ── Test from_string ────────────────────────────────────
    print("\n=== from_string ===")
    b1 = Book.from_string("B001,Clean Code,Robert Martin,699,Programming")
    b2 = Book.from_string("B002,Atomic Habits,James Clear,399,Self-Help")
    print(b1)
    # Expected: [B001] Clean Code — Robert Martin | Rs.699 | Genre: Programming | Available
    print(b2)
    # Expected: [B002] Atomic Habits — James Clear | Rs.399 | Genre: Self-Help | Available

    # ── Test load_catalog ───────────────────────────────────
    print("\n=== load_catalog ===")
    raw_data = [
        "B001,Clean Code,Robert Martin,699,Programming",
        "B002,Atomic Habits,James Clear,399,Self-Help",
        "B003,The Pragmatic Programmer,David Thomas,799,Programming",
        "B004,Deep Work,Cal Newport,299,Productivity",
    ]
    catalog = load_catalog(raw_data)
    print(f"Total books loaded: {len(catalog)}")  # 4
    for book_id, book in catalog.items():
        print(book)
    # Expected output (one per line):
    # [B001] Clean Code — Robert Martin | Rs.699 | Genre: Programming | Available
    # [B002] Atomic Habits — James Clear | Rs.399 | Genre: Self-Help | Available
    # [B003] The Pragmatic Programmer — David Thomas | Rs.799 | Genre: Programming | Available
    # [B004] Deep Work — Cal Newport | Rs.299 | Genre: Productivity | Available

    # ── Bonus: from_string still supports == and < ──────────
    print("\n=== Bonus: operators still work after from_string ===")
    b3 = Book.from_string("B001,Clean Code,Robert Martin,699,Programming")
    print(b1 == b3)   # True  (same book_id)
    print(b2 < b1)    # True  (399 < 699)
