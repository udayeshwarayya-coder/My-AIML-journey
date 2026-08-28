from flask import Flask, request, jsonify, send_from_directory
import random
from datetime import datetime
import os
app=Flask(__name__)
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
class EBook(Book):
    def __init__(self, book_id, title, author, price, genre, download_link="No link found", available=True):
        super().__init__(book_id, title, author, price, genre, available)
        self.download_link = download_link
    def __str__(self):
            # YOUR CODE HERE
            s=super().__str__()
            return f"{s}|Link:{self.download_link}"
    def __repr__(self):
            return (f'EBook(book_id="{self.book_id}", title="{self.title}", '
                    f'author="{self.author}", price={self._price}, '
                    f'genre="{self.genre}", available={self.available}, '
                    f'download_link="{self.download_link}")')
    @classmethod
    def from_string(cls, data_string):
            # YOUR CODE HERE
            d = data_string.strip().split(",")
            return cls(d[0], d[1], d[2], int(d[3]), d[4], d[5])
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

book_rows=["B001,Atomic Habits,James Clear,399,Self-Help",
        "B002,Deep Work,Cal Newport,299,Productivity",]
ebook_rows=["E001,Clean Code,Robert Martin,499,Programming,http://books.com/cc",
        "E002,The Pragmatic Programmer,David Thomas,599,Programming,http://books.com/pp",]
catalog = load_mixed_catalog(book_rows, ebook_rows)

@app.route("/")
def home():
     return send_from_directory(" ")

@app.route("/api/books", methods=["GET"])
def load_books():
    return jsonify(catalog)

@app.route("/api/avilable",methods=["POST"])
def check_available():
    data=request.args.get("book_id",None)
    if data in catalog:
        for d in catalog.values():
            if d["book_id"]==data["book_id"]:
                if d["available"]:
                    return jsonify({"message":"available"})
                else:
                    return jsonify({"message":"not available"})
    else:
        return jsonify({"message":"book_id invalid"})
    





