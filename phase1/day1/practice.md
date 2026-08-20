# ✏️ Day 1 — Practice Tasks

**Topic:** Classes, Objects, and the `__init__` method  
**Estimated Time:** ~20-25 minutes  
**Instructions:** Create a file called `practice.py` and solve each task in it.

---

## Task 1: Create a Simple Class 🟢 (Easy)

Create a class called `Person` with:
- `name` (string)
- `age` (int)
- A method `greet()` that prints: `"Hi, I'm {name} and I'm {age} years old."`

**Test it:**
```python
p1 = Person("Uday", 19)
p1.greet()  # Hi, I'm Uday and I'm 19 years old.
```

---

## Task 2: Class with Default Values 🟢 (Easy)

Create a class called `Rectangle` with:
- `length` (default = 1)
- `width` (default = 1)
- A method `area()` that returns the area
- A method `perimeter()` that returns the perimeter

**Test it:**
```python
r1 = Rectangle(5, 3)
print(r1.area())       # 15
print(r1.perimeter())  # 16

r2 = Rectangle()  # uses defaults
print(r2.area())       # 1
```

---

## Task 3: Student Report Card 🟡 (Medium)

Create a class called `Student` with:
- `name`, `marks` (a list of integers)
- A method `average()` that returns the average marks
- A method `grade()` that returns:
  - `"A"` if average >= 90
  - `"B"` if average >= 75
  - `"C"` if average >= 60
  - `"F"` otherwise

**Test it:**
```python
s1 = Student("Uday", [85, 92, 78, 95, 88])
print(s1.average())  # 87.6
print(s1.grade())    # B
```

---

## Task 4: Bank Account 🟡 (Medium)

Create a class called `BankAccount` with:
- `owner` (string), `balance` (float, default = 0)
- `deposit(amount)` — adds to balance
- `withdraw(amount)` — subtracts from balance, but prints `"Insufficient funds!"` if amount > balance
- `display()` — prints `"Account owner: {owner} | Balance: ₹{balance}"`

**Test it:**
```python
acc = BankAccount("Uday", 5000)
acc.deposit(2000)
acc.withdraw(1500)
acc.withdraw(10000)  # Insufficient funds!
acc.display()        # Account owner: Uday | Balance: ₹5500
```

---

## Task 5: Class Variable Counter 🟠 (Medium-Hard)

Create a class called `Employee` with:
- A **class variable** `count` that tracks total employees created
- Instance variables: `name`, `department`
- Every time an object is created, `count` should increase by 1
- A **class method** or regular method `get_count()` that returns total employees

**Test it:**
```python
e1 = Employee("Uday", "Engineering")
e2 = Employee("Ravi", "Marketing")
e3 = Employee("Sneha", "Design")
print(Employee.count)  # 3
```

> 💡 Hint: Increment the class variable inside `__init__`.

---

## Task 6: Mini Project — Book Library 🔴 (Challenge)

Create a class called `Book` with:
- `title`, `author`, `pages`, `is_read` (default = False)
- `mark_read()` — sets `is_read` to True
- `info()` — returns a string like: `"'The Alchemist' by Paulo Coelho — 197 pages — ✅ Read"` or `"❌ Not Read"`

Then create a class called `Library` with:
- `name`, `books` (an empty list initially)
- `add_book(book)` — adds a Book object to the list
- `list_books()` — prints all books using their `info()` method
- `unread_books()` — returns a list of books that haven't been read yet

**Test it:**
```python
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
```

---

## ✅ Checklist

- [ ] Task 1: Person class
- [ ] Task 2: Rectangle class
- [ ] Task 3: Student Report Card
- [ ] Task 4: Bank Account
- [ ] Task 5: Class Variable Counter
- [ ] Task 6: Book Library (Challenge)

> When done, share your `practice.py` file and I'll review it! 🚀
