import sys
import io
import os
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ─────────────────────────────────────────────
#  Flask App
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR)


# ─────────────────────────────────────────────
#  Book Classes
# ─────────────────────────────────────────────
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

    def to_dict(self):
        return {
            "book_id":   self.book_id,
            "title":     self.title,
            "author":    self.author,
            "price":     self._price,
            "genre":     self.genre,
            "available": self.available,
            "type":      "book",
        }


class EBook(Book):
    def __init__(self, book_id, title, author, price, genre, download_link="No link found", available=True):
        super().__init__(book_id, title, author, price, genre, available)
        self.download_link = download_link

    def __str__(self):
        s = super().__str__()
        return f"{s} | Link: {self.download_link}"

    def __repr__(self):
        return (f'EBook(book_id="{self.book_id}", title="{self.title}", '
                f'author="{self.author}", price={self._price}, '
                f'genre="{self.genre}", available={self.available}, '
                f'download_link="{self.download_link}")')

    @classmethod
    def from_string(cls, data_string):
        d = data_string.strip().split(",")
        return cls(d[0], d[1], d[2], int(d[3]), d[4], d[5])

    def to_dict(self):
        d = super().to_dict()
        d["download_link"] = self.download_link
        d["type"] = "ebook"
        return d


# ─────────────────────────────────────────────
#  Catalog Loader
# ─────────────────────────────────────────────
def load_mixed_catalog(book_rows, ebook_rows):
    catalog = {}
    for row in book_rows:
        b = Book.from_string(row)
        catalog[b.book_id] = b
    for row in ebook_rows:
        eb = EBook.from_string(row)
        catalog[eb.book_id] = eb
    return catalog


book_rows = [
    "B001,Atomic Habits,James Clear,399,Self-Help",
    "B002,Deep Work,Cal Newport,299,Productivity",
    "B003,The Alchemist,Paulo Coelho,249,Fiction",
    "B004,Rich Dad Poor Dad,Robert Kiyosaki,349,Self-Help",
]
ebook_rows = [
    "E001,Clean Code,Robert Martin,499,Programming,https://books.com/clean-code",
    "E002,The Pragmatic Programmer,David Thomas,599,Programming,https://books.com/pragmatic",
    "E003,Python Crash Course,Eric Matthes,449,Programming,https://books.com/python-crash",
]

catalog = load_mixed_catalog(book_rows, ebook_rows)

# Auto-increment counter for new book IDs
_book_counter = len([k for k in catalog if k.startswith("B")])
_ebook_counter = len([k for k in catalog if k.startswith("E")])


# ─────────────────────────────────────────────
#  Routes — Frontend
# ─────────────────────────────────────────────
@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


# ─────────────────────────────────────────────
#  Routes — API
# ─────────────────────────────────────────────

@app.route("/api/books", methods=["GET"])
def get_books():
    """Return all books as a list of dicts."""
    return jsonify([book.to_dict() for book in catalog.values()])


@app.route("/api/books", methods=["POST"])
def add_book():
    """Add a new Book or EBook to the catalog."""
    global _book_counter, _ebook_counter
    data = request.get_json()

    required = ["title", "author", "price", "genre"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    if not Book.is_valid_price(data["price"]):
        return jsonify({"error": "Price must be a positive number"}), 400

    book_type = data.get("type", "book").lower()

    if book_type == "ebook":
        _ebook_counter += 1
        book_id = f"E{_ebook_counter:03d}"
        new_book = EBook(
            book_id   = book_id,
            title     = data["title"],
            author    = data["author"],
            price     = data["price"],
            genre     = data["genre"],
            download_link = data.get("download_link", "No link found"),
        )
    else:
        _book_counter += 1
        book_id = f"B{_book_counter:03d}"
        new_book = Book(
            book_id = book_id,
            title   = data["title"],
            author  = data["author"],
            price   = data["price"],
            genre   = data["genre"],
        )

    catalog[book_id] = new_book
    return jsonify(new_book.to_dict()), 201


@app.route("/api/available", methods=["GET"])
def check_available():
    """Check if a book is available by book_id."""
    book_id = request.args.get("book_id", None)
    if not book_id:
        return jsonify({"error": "book_id parameter is required"}), 400
    if book_id not in catalog:
        return jsonify({"error": "Book not found"}), 404
    book = catalog[book_id]
    return jsonify({"book_id": book_id, "available": book.available})


@app.route("/api/books/<book_id>/issue", methods=["PUT"])
def issue_book(book_id):
    """Mark a book as issued."""
    if book_id not in catalog:
        return jsonify({"error": "Book not found"}), 404
    book = catalog[book_id]
    if not book.available:
        return jsonify({"error": "Book is already issued"}), 409
    book.available = False
    return jsonify({"message": f'"{book.title}" has been issued.', "book": book.to_dict()})


@app.route("/api/books/<book_id>/return", methods=["PUT"])
def return_book(book_id):
    """Mark a book as returned (available)."""
    if book_id not in catalog:
        return jsonify({"error": "Book not found"}), 404
    book = catalog[book_id]
    if book.available:
        return jsonify({"error": "Book is already available (not issued)"}), 409
    book.available = True
    return jsonify({"message": f'"{book.title}" has been returned.', "book": book.to_dict()})


@app.route("/api/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    """Delete a book from the catalog."""
    if book_id not in catalog:
        return jsonify({"error": "Book not found"}), 404
    removed = catalog.pop(book_id)
    return jsonify({"message": f'"{removed.title}" deleted successfully.'})


@app.route("/api/search", methods=["GET"])
def search_books():
    """Search books by title, author, or genre (case-insensitive)."""
    query = request.args.get("q", "").lower().strip()
    if not query:
        return jsonify([book.to_dict() for book in catalog.values()])
    results = [
        book.to_dict() for book in catalog.values()
        if query in book.title.lower()
        or query in book.author.lower()
        or query in book.genre.lower()
    ]
    return jsonify(results)


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Return summary statistics."""
    books  = [b for b in catalog.values() if b.__class__.__name__ == "Book"]
    ebooks = [b for b in catalog.values() if b.__class__.__name__ == "EBook"]
    total  = len(catalog)
    avail  = sum(1 for b in catalog.values() if b.available)
    return jsonify({
        "total":     total,
        "available": avail,
        "issued":    total - avail,
        "books":     len(books),
        "ebooks":    len(ebooks),
    })


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
