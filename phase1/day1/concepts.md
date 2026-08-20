# 📘 Day 1 — Introduction to Classes & Objects

**Phase:** 1 (Python OOPs & Advanced Core)  
**Topic:** Classes, Objects, and the `__init__` method  
**Time:** ~30 minutes  

---

## 🧠 What You'll Learn Today

1. What are Classes and Objects?
2. How to define a Class
3. How to create Objects (instances)
4. The `__init__` method (constructor)
5. Instance variables vs Class variables
6. The `self` keyword

---

## 1. What are Classes and Objects?

Think of a **Class** as a **blueprint** and an **Object** as a **real thing built from that blueprint**.

| Concept | Real-World Analogy |
|---------|-------------------|
| Class   | Blueprint of a Car |
| Object  | An actual Car (Red Honda, Blue Toyota) |

```python
# A class is just a template
class Car:
    pass

# Objects are real instances created from that template
my_car = Car()
your_car = Car()

print(type(my_car))  # <class '__main__.Car'>
```

> **Key Insight:** A class defines *what something is*, an object *is* that thing.

---

## 2. Defining a Class

Use the `class` keyword. Class names use **PascalCase** (first letter of each word capitalized).

```python
class Student:
    pass  # empty class for now
```

**Naming conventions:**
- ✅ `Student`, `BankAccount`, `ShoppingCart`
- ❌ `student`, `bank_account`, `shopping_cart` (these are for variables/functions)

---

## 3. The `__init__` Method (Constructor)

`__init__` is a special method that runs **automatically** when you create an object. It's used to set up initial values.

```python
class Student:
    def __init__(self, name, age, grade):
        self.name = name      # instance variable
        self.age = age         # instance variable
        self.grade = grade     # instance variable

# Creating objects — __init__ runs automatically here
s1 = Student("Uday", 19, "A")
s2 = Student("Ravi", 20, "B")

print(s1.name)   # Uday
print(s2.grade)  # B
```

> **Why `__init__`?** Without it, every object would be empty. `__init__` lets you give each object its own unique data at creation.

---

## 4. The `self` Keyword

`self` refers to the **current object** being created or used. It's how Python knows which object's data to work with.

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name    # self.name = this specific dog's name
        self.breed = breed

    def bark(self):
        print(f"{self.name} says Woof!")  # self.name = THIS dog's name

dog1 = Dog("Buddy", "Golden Retriever")
dog2 = Dog("Max", "German Shepherd")

dog1.bark()  # Buddy says Woof!
dog2.bark()  # Max says Woof!
```

> **Think of `self` as "me".** When `dog1` calls `bark()`, `self` = `dog1`. When `dog2` calls it, `self` = `dog2`.

---

## 5. Instance Variables vs Class Variables

| Type | Belongs to | Shared? | Where defined? |
|------|-----------|---------|----------------|
| Instance Variable | Each object | ❌ No, unique per object | Inside `__init__` with `self.` |
| Class Variable | The class itself | ✅ Yes, shared by all objects | Directly inside class body |

```python
class Student:
    school = "ABC Academy"  # Class variable — shared by ALL students

    def __init__(self, name, roll_no):
        self.name = name        # Instance variable — unique per student
        self.roll_no = roll_no  # Instance variable — unique per student

s1 = Student("Uday", 101)
s2 = Student("Ravi", 102)

print(s1.school)    # ABC Academy
print(s2.school)    # ABC Academy  (same for both!)
print(s1.name)      # Uday
print(s2.name)      # Ravi         (different!)
```

---

## 6. Adding Methods to a Class

Methods are just functions inside a class. They always take `self` as the first parameter.

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited ₹{amount}. New balance: ₹{self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds!")
        else:
            self.balance -= amount
            print(f"Withdrew ₹{amount}. New balance: ₹{self.balance}")

    def get_balance(self):
        return self.balance

# Usage
acc = BankAccount("Uday", 1000)
acc.deposit(500)      # Deposited ₹500. New balance: ₹1500
acc.withdraw(200)     # Withdrew ₹200. New balance: ₹1300
acc.withdraw(5000)    # Insufficient funds!
```

---

## 📌 Quick Recap

```
Class       → Blueprint / Template
Object      → Real instance created from a class
__init__    → Constructor, runs when object is created
self        → Refers to the current object ("me")
Instance var → Unique to each object (self.name)
Class var    → Shared across all objects (defined in class body)
Methods      → Functions inside a class (always take self)
```
