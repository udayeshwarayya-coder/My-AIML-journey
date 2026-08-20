# class Person:
#     def __init__(self,name,age):
#         self.name=name
#         self.age=age
#     def greet(self):
#         print(f"hi i am {self.name} my age is {self.age}")
# p1=Person("uday",19)
# p1.greet()
        

# 2
# class Rectangle:
#     def __init__(self,l=1,b=1):
#         self.length=l
#         self.bright=b
#     def area(self):
#         result=self.length*self.bright
#         return f"area of rectangle is {result}"
#     def perimeter(self):
#         result=2*(self.length*self.bright)
#         return f"perimeter of rectangle is{result}"
        
# r1 = Rectangle(5, 3)
# print(r1.area())       # 15
# print(r1.perimeter())  # 16

# r2 = Rectangle()  # uses defaults
# print(r2.area())
# print(r2.perimeter())       # 1


# 3

# class Student:
    
#     def __init__(self, name, marks):
#         self.name=name
#         self.marks=marks
#     def average(self):
#         total=0
#         for m in self.marks:
#             total+=m
        
#         return total/len(self.marks)
#     def grade(self):
#         grade=""
#         if self.average()>=90:
#             grade='A'
#         elif self.average()>=75:
#             grade='B'
#         elif self.average()>=60:
#             grade='C'
#         else:
#             grade='F'
#         return grade

# s1 = Student("Uday", [85, 92, 78, 95, 88])
# print(s1.average())  # 87.6
# print(s1.grade())    # B


# 4

# class BankAccount:
#     def __init__(self, owner, balance=0):
#         self.owner = owner
#         self.balance=balance
#     def deposit(self, amount):
#         self.balance+=amount
#         print(f"balance remaining {self.balance}")
#     def withdraw(self, amount):
#         if amount>self.balance:
#             print("Insuficient funds!")
#         else:
#             self.balance-=amount
#             print(f"balance remaining {self.balance}")
#     def display(self):
#         print(f"Account owner: {self.owner} | Balance:{self.balance}")
# acc = BankAccount("Uday", 5000)
# acc.deposit(2000)
# acc.withdraw(1500)
# acc.withdraw(10000)  # Insufficient funds!
# acc.display()        # Account owner: Uday | Balance: ₹5500


# 5
# Create a class called `Employee` with:
# - A **class variable** `count` that tracks total employees created
# - Instance variables: `name`, `department`
# - Every time an object is created, `count` 
# should increase by 1
# - A **class method** or regular method `get_count()`
# that returns total employees

# **Test it:**
# ```python
# class Employee:
#     count = 0
#     def __init__(self, name, department):
#         self.name = name
#         self.department = department
#         Employee.count += 1
#     def get_count(self):
#         return Employee.count
        
# e1 = Employee("Uday", "Engineering")
# e2 = Employee("Ravi", "Marketing")
# e3 = Employee("Sneha", "Design")
# print(Employee.count)  # 3


# 6


# Then create a class called `Library` with:
# - `name`, `books` (an empty list initially)
# - `add_book(book)` — adds a Book object to the list
# - `list_books()` — prints all books using their `info()` method
# - `unread_books()` — returns a list of books that haven't been read yet

# **Test it:**
# ```python
class Book:
    def __init__(self, title, author,pages,is_read='false'):
        self.title=title
        self.author=author
        self.pages=pages
        self.is_read=is_read
    def mark_read(self):
        self.is_read='true'
    def info(self):
        if self.is_read == "true":
            return f"'{self.title}' by {self.author} — {self.pages} pages — ✅ Read"
        else:
            return f"'{self.title}' by {self.author} — {self.pages} pages — ❌ Not"

class Library:
    def __init__(self,name):
        self.name=name
        self.books=[]
    def add_book(self, book):
        if book not in self.books:
            self.books.append(book)
            print(f"Book '{book.title}' added to the library.")
    def list_books(self):
        for book in self.books:
            print(book.info())

    def unread_books(self):
        return [book for book in self.books if not book.is_read]
        
b1 = Book("The Alchemist", "Paulo Coelho", 197)
b2 = Book("Atomic Habits", "James Clear", 320)
b3 = Book("Deep Work", "Cal Newport", 296)

lib = Library("My Library")
lib.add_book(b1)
lib.add_book(b2)
lib.add_book(b3)

b1.mark_read()

lib.list_books()
# 'The Alchemist' by Paulo Coelho — 197 pages — ✅ Read
# 'Atomic Habits' by James Clear — 320 pages — ❌ Not Read
# 'Deep Work' by Cal Newport — 296 pages — ❌ Not Read

print(len(lib.unread_books()))  # 2
