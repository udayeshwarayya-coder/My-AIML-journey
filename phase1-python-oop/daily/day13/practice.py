# Day 13 Practice — Magic Methods: __str__ and __repr__
# Project 4: Library Management System
# Topic: Dunder methods, string representation of objects
# Goal: Write the Book class + 2 catalog functions

# ============================================================
# CATALOG FORMAT (dict keyed by book_id):
# {
#   "B001": <Book object>,
#   "B002": <Book object>,
# }
# ============================================================


# ============================================================
# TASK 1: Book Class
# ============================================================
# Attributes:
#   book_id, title, author, _price (private), genre, available (bool, default=True)
#
# Methods:
#   @property price  +  @price.setter  (reject negative prices)
#   __str__  →  "[B001] Clean Code — Robert Martin | Rs.699 | Genre: Programming | Available"
#   __repr__ →  Book(book_id="B001", title="Clean Code", author="Robert Martin", price=699, genre="Programming", available=True)

class Book:
    def __init__(self, book_id, title, author, price, genre, available=True):
        # YOUR CODE HERE
        self.book_id=book_id
        self.title=title
        self.author=author
        self.price=price
        self.genre=genre
        self.available=available

    @property
    def price(self):
        # YOUR CODE HERE
        return self._price

    @price.setter
    def price(self, new_price):
        # YOUR CODE HERE
        if new_price >0:
            self._price=new_price
        
    def __str__(self):
        # YOUR CODE HERE
        if self.available:
            return f"[{self.book_id}]{self.title}-{self.author}|Rs.{self.price}|Genre:{self.genre}|Available"
        else:
            return f"[{self.book_id}]{self.title}-{self.author}|Rs.{self.price}|Genre:{self.genre}|not Available"
    def __repr__(self):
        # YOUR CODE HERE
        return f"Book(book_id={self.book_id},title={self.title},author={self.author}, price={self.price}, genre={self.genre}, available={self.available})"


# ============================================================
# TASK 2: add_book(catalog, book)
# ============================================================
# - If book_id already in catalog: print a message, do NOT overwrite
# - Else: add it and print confirmation using print(book)
# Return: updated catalog

def add_book(catalog, book):
    # YOUR CODE HERE
    if book.book_id not in catalog:
        catalog[book.book_id]=book
        print(f"updated  catalog {book}")
        
    else:
        print("do not overwrite")
        
    return catalog

# ============================================================
# TASK 3: display_catalog(catalog)
# ============================================================
# - Handle empty catalog case
# - Print a header, loop and print each book, print a footer
# Return: None

def display_catalog(catalog):
    # YOUR CODE HERE
    if not catalog:
        print("Catalog is empty.")
        return
    print("=" * 60)
    print("LIBRARY CATALOG")
    print("=" * 60)
    for book in catalog.values():
        print(book)
    print("=" * 60)



# ============================================================
# TEST YOUR CODE — run: python practice.py
# ============================================================

if __name__ == "__main__":

    b1 = Book("B001", "Clean Code", "Robert Martin", 699, "Programming")
    b2 = Book("B002", "Atomic Habits", "James Clear", 399, "Self-Help", available=False)
    b3 = Book("B003", "The Pragmatic Programmer", "David Thomas", 799, "Programming")
    b4 = Book("B004", "Deep Work", "Cal Newport", 299, "Productivity")

    # Test __str__
    print(b1)
    print(b2)

    # Test __repr__
    print(repr(b1))
    print([b1, b2])

    # Test price setter
    b1.price = 750
    print(f"Updated price: Rs.{b1.price}")
    try:
        b1.price = -100
    except ValueError as e:
        print(f"Caught: {e}")
    b1.price = 699

    # Test add_book
    catalog = {}
    add_book(catalog, b1)
    add_book(catalog, b2)
    add_book(catalog, b3)
    add_book(catalog, b4)
    add_book(catalog, b1)   # duplicate — should NOT add

    # Test display_catalog
    print()
    display_catalog(catalog)
    print()
    display_catalog({})     # empty case
