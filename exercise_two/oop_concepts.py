"""
Exercise Two: Object-Oriented Programming (OOP) in Python
==========================================================

Object-Oriented Programming, usually called OOP, is a way of writing programs
by grouping related data and related behavior together in one place.

In simple words:
    - Data means values like name, age, salary, balance, color, etc.
    - Behavior means actions like introduce(), deposit(), withdraw(), start(), etc.

Instead of writing everything as separate variables and separate functions,
OOP helps us build real-world style models such as Student, Car, BankAccount,
Employee, Dog, Vehicle, and many more.

Why OOP is useful:
    - It makes code easier to organize.
    - It makes large programs easier to manage.
    - It improves reusability, because one class can be reused many times.
    - It improves readability, because related code stays together.
    - It helps break big problems into smaller logical parts.

OOP organizes code using:
  - Classes      → blueprints
  - Objects      → real things made from blueprints
  - Attributes   → data stored inside an object
  - Methods      → actions an object can perform

Think of it like this:
    - A class is the design.
    - An object is the actual item created from that design.
    - Attributes describe the object.
    - Methods define what the object can do.

Four Pillars of OOP:
  1. Encapsulation  → hide and protect data
  2. Inheritance    → reuse code from parent class
  3. Polymorphism   → same method name, different behavior
  4. Abstraction    → hide complexity, show only what matters

This file explains each concept one by one with simple examples.
Read the comments first, then observe the code, then compare the output.
"""

# =============================================================================
# 1. CLASS AND OBJECT
# =============================================================================
# Theory:
# A class is a blueprint or template used to create objects.
# It defines what data an object will have and what actions it can perform.
#
# An object is an actual instance created from a class.
# If Student is a class, then Rahul and Priya are objects of that class.
#
# Real-life idea:
#   - Class  -> Car
#   - Object -> BMW, Audi, Tesla
#
# A class does not represent one real item.
# It represents the common structure for many similar items.


class Student:

    def __init__(
        self, name, age
    ):  # Constructor — runs automatically when object is created
        self.name = name  # Instance attribute
        self.age = age  # Instance attribute

    def introduce(self):  # Instance method
        print(f"Hi, I am {self.name} and I am {self.age} years old.")


# Creating objects (instances) from the Student class
s1 = Student("Rahul", 20)
s2 = Student("Priya", 22)

print("--- 1. Class and Object ---")
s1.introduce()  # Hi, I am Rahul and I am 20 years old.
s2.introduce()  # Hi, I am Priya and I am 22 years old.
print()


# =============================================================================
# 2. CONSTRUCTOR (__init__)
# =============================================================================
# Theory:
# __init__() is a special method called a constructor.
# Python runs it automatically whenever a new object is created.
#
# Its main job is to give initial values to the object.
# For example, when we create Mobile("iPhone", 80000), those values are
# received by __init__() and stored inside the new object.
#
# Important point:
# __init__() is optional. If you do not write it, Python can still create
# the object, but the object will not get custom starting values automatically.


class Mobile:

    def __init__(self, brand, price):
        self.brand = brand
        self.price = price

    def show_details(self):
        print(f"Brand: {self.brand} | Price: ₹{self.price}")


print("--- 2. Constructor (__init__) ---")
m1 = Mobile("iPhone", 80000)
m2 = Mobile("Samsung", 45000)

m1.show_details()  # Brand: iPhone | Price: ₹80000
m2.show_details()  # Brand: Samsung | Price: ₹45000
print()


# =============================================================================
# 3. SELF
# =============================================================================
# Theory:
# 'self' refers to the current object.
# It helps Python know which object's data should be used.
#
# Example:
# If c1.show_color() is called, 'self' refers to c1.
# If c2.show_color() is called, 'self' refers to c2.
#
# That is why the same method can work for many objects.
# Each object uses its own data through 'self'.
#
# Internally:
#   c1.show_color()
# becomes something like:
#   Car.show_color(c1)
#
# That is why 'self' must be the first parameter in instance methods.


class Car:

    def __init__(self, color):
        self.color = color  # self.color belongs to THIS specific object

    def show_color(self):
        print(f"This car is {self.color}.")


print("--- 3. Self ---")
c1 = Car("Red")
c2 = Car("Blue")

c1.show_color()  # This car is Red.
c2.show_color()  # This car is Blue.
print()


# =============================================================================
# 4. INSTANCE VARIABLES
# =============================================================================
# Theory:
# Variables created with self.variable_name are called instance variables.
# They belong to a specific object, not to the whole class.
#
# This means each object stores its own separate values.
# For example, d1 has its own name and breed, and d2 has different values.
#
# This is one of the biggest strengths of OOP:
# we can create many objects from one class, and every object can hold
# different data while using the same methods.


class Dog:

    def __init__(self, name, breed):
        self.name = name  # unique to each dog object
        self.breed = breed  # unique to each dog object

    def bark(self):
        print(f"{self.name} ({self.breed}) says: Woof!")


print("--- 4. Instance Variables ---")
d1 = Dog("Bruno", "Labrador")
d2 = Dog("Tommy", "Pug")

d1.bark()  # Bruno (Labrador) says: Woof!
d2.bark()  # Tommy (Pug) says: Woof!
print()


# =============================================================================
# 5. ENCAPSULATION
# =============================================================================
# Theory:
# Encapsulation means wrapping data and methods together in one unit,
# and protecting important data from direct outside access.
#
# In simple words, some values should not be changed carelessly from outside.
# For example, a bank balance should be updated through deposit() or withdraw(),
# not by directly changing the balance variable from anywhere in the program.
#
# In Python, using double underscore like __balance makes the variable private.
# That means we should access it through class methods.
#
# Benefit of encapsulation:
#  - better safety
#  - better control over data
#  - easier debugging
#  - cleaner code design


class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # Private variable — cannot be accessed directly

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"₹{amount} deposited. New balance: ₹{self.__balance}")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient funds.")
        else:
            self.__balance -= amount
            print(f"₹{amount} withdrawn. Remaining balance: ₹{self.__balance}")

    def show_balance(self):
        print(f"Account owner: {self.owner} | Balance: ₹{self.__balance}")


print("--- 5. Encapsulation ---")
acc = BankAccount("Aarav", 10000)
acc.deposit(5000)  # ₹5000 deposited. New balance: ₹15000
acc.withdraw(3000)  # ₹3000 withdrawn. Remaining balance: ₹12000
acc.show_balance()  # Account owner: Aarav | Balance: ₹12000

# acc.__balance  ← This would throw AttributeError (private variable — protected!)
print()


# =============================================================================
# 6. INHERITANCE
# =============================================================================
# Theory:
# Inheritance allows one class to use features of another class.
#
# The class that gives features is called the parent class or base class.
# The class that receives features is called the child class or derived class.
#
# This helps avoid repeating the same code again and again.
# If many classes share common behavior, we can put that common code in one
# parent class and let child classes reuse it.
#
# Example:
# Animal can contain common behavior like breathe() and eat().
# Dog and Cat can inherit those common behaviors and also add their own methods.


class Animal:  # Parent class

    def __init__(self, name):
        self.name = name

    def breathe(self):
        print(f"{self.name} breathes oxygen.")

    def eat(self):
        print(f"{self.name} eats food.")


class Dog(Animal):  # Child class — inherits from Animal

    def bark(self):
        print(f"{self.name} says: Woof!")


class Cat(Animal):  # Child class — inherits from Animal

    def meow(self):
        print(f"{self.name} says: Meow!")


print("--- 6. Inheritance ---")
dog = Dog("Bruno")
cat = Cat("Whiskers")

dog.breathe()  # Inherited from Animal → Bruno breathes oxygen.
dog.eat()  # Inherited from Animal → Bruno eats food.
dog.bark()  # Dog's own method    → Bruno says: Woof!

cat.breathe()  # Inherited from Animal → Whiskers breathes oxygen.
cat.meow()  # Cat's own method     → Whiskers says: Meow!
print()


# =============================================================================
# 7. POLYMORPHISM
# =============================================================================
# Theory:
# Polymorphism means "many forms".
# In OOP, it means the same method name can behave differently for different
# objects or classes.
#
# This is useful because the programmer can use one common interface,
# such as sound(), and each object can decide its own behavior.
#
# So even though Bird, Dog, and Cat all use sound(), the result is different.
# This makes code flexible and easier to extend.


class Bird:

    def sound(self):
        print("Bird chirps: Tweet Tweet")


class Dog:

    def sound(self):
        print("Dog barks: Woof Woof")


class Cat:

    def sound(self):
        print("Cat meows: Meow Meow")


print("--- 7. Polymorphism ---")
animals = [Bird(), Dog(), Cat()]

for animal in animals:
    animal.sound()  # Same method name 'sound()' — different output for each
print()


# =============================================================================
# 8. ABSTRACTION
# =============================================================================
# Theory:
# Abstraction means hiding unnecessary internal details and showing only the
# essential idea to the user.
#
# In real life, when we drive a car, we use steering, brake, and accelerator.
# We do not need to know every internal engine detail to drive it.
#
# In programming, abstraction helps us define what something should do,
# without forcing the user to know how it is implemented.
#
# Python provides abstraction through the abc module.
# An abstract class can define required methods, and child classes must
# implement those methods.
#
# Important words in this section:
#   - Abstract class:
#       A class that acts like a rule book or template.
#       We do not create objects directly from it.
#       Its purpose is to say what child classes MUST provide.
#
#   - Abstract method:
#       A method declared in the abstract class without full implementation.
#       It forces every child class to write its own version of that method.
#
#   - Concrete class:
#       A normal child class that gives actual implementation to all required
#       abstract methods. Objects can be created from concrete classes.

from abc import ABC, abstractmethod


class Vehicle(ABC):  # Abstract class — a blueprint with rules for child classes
    # We inherit from ABC to tell Python that Vehicle is abstract
    # and should not be used to create direct objects.

    @abstractmethod  # Marks this method as mandatory for child classes
    def start(
        self,
    ):  # Abstract method — Vehicle says every vehicle must know how to start
        pass

    @abstractmethod  # Marks this method as mandatory for child classes
    def stop(
        self,
    ):  # Abstract method — Vehicle says every vehicle must know how to stop
        pass


class Bike(
    Vehicle
):  # Concrete class — provides real implementation of all abstract methods

    def start(self):
        print("Bike starts: Turn the key and press the starter.")

    def stop(self):
        print("Bike stops: Apply brakes.")


class ElectricCar(
    Vehicle
):  # Concrete class — another child class with its own implementation

    def start(self):
        print("Electric Car starts: Press the power button.")

    def stop(self):
        print("Electric Car stops: Regenerative braking applied.")


print("--- 8. Abstraction ---")
bike = Bike()
ecar = ElectricCar()

bike.start()  # Bike starts: Turn the key and press the starter.
bike.stop()  # Bike stops: Apply brakes.
ecar.start()  # Electric Car starts: Press the power button.
ecar.stop()  # Electric Car stops: Regenerative braking applied.

# vehicle = Vehicle()  ← This would throw TypeError because abstract classes are incomplete.
#                        They only define rules, so Python does not allow direct objects from them.
print()


# =============================================================================
# 9. TYPES OF METHODS
# =============================================================================
# Theory:
# Python classes mainly use three kinds of methods:
#
# 1. Instance method:
#    Works with object-specific data.
#    Uses 'self'.
#
# 2. Class method:
#    Works with class-level data shared by all objects.
#    Uses 'cls'.
#
# 3. Static method:
#    A utility method related to the class, but independent from both
#    object data and class data.
#
# Understanding the difference between these three is important because it
# helps you decide whether a method should work on one object, the whole class,
# or just perform a helper task.


class School:

    school_name = "Sunrise Academy"  # Class variable — shared by all objects

    def __init__(self, student_name):
        self.student_name = student_name  # Instance variable — unique to each object

    # Instance Method — works with object-specific data (uses self)
    def show_student(self):
        print(f"Student: {self.student_name}")

    # Class Method — works with class-level data (uses cls)
    @classmethod
    def show_school(cls):
        print(f"School: {cls.school_name}")

    # Static Method — independent utility; does not use self or cls
    @staticmethod
    def greet():
        print("Welcome to our school!")


print("--- 9. Types of Methods ---")
st1 = School("Mrunmay")

st1.show_student()  # Instance method  → Student: Mrunmay
School.show_school()  # Class method     → School: Sunrise Academy
School.greet()  # Static method    → Welcome to our school!
print()


# =============================================================================
# 10. COMPLETE REAL-WORLD EXAMPLE — Employee Management System
# =============================================================================
# Theory:
# This final example combines multiple OOP ideas together in one program.
#
# It shows:
#  - a class variable shared by all employees
#  - a constructor to initialize objects
#  - encapsulation using a private salary variable
#  - inheritance through Developer and Designer classes
#  - polymorphism by overriding show_details()
#  - class method and static method usage
#
# This is how OOP is commonly used in real projects.
# Instead of isolated examples, we build connected classes that model a system.


class Employee:

    company = "TechCorp"  # Class variable

    def __init__(self, name, salary):
        self.name = name
        self.__salary = salary  # Private — encapsulated

    def show_details(self):
        print(
            f"Name: {self.name} | Company: {Employee.company} | Salary: ₹{self.__salary}"
        )

    def give_raise(self, amount):
        self.__salary += amount
        print(
            f"{self.name} received a raise of ₹{amount}. New salary: ₹{self.__salary}"
        )

    @classmethod
    def company_info(cls):
        print(f"Company: {cls.company}")

    @staticmethod
    def work_hours():
        print("Standard work hours: 9 AM to 6 PM")


class Developer(Employee):  # Inherits from Employee

    def __init__(self, name, salary, language):
        super().__init__(name, salary)  # Call parent constructor
        self.language = language

    def show_details(self):  # Polymorphism — overrides parent method
        super().show_details()
        print(f"Primary Language: {self.language}")

    def code(self):
        print(f"{self.name} is writing code in {self.language}.")


class Designer(Employee):  # Inherits from Employee

    def __init__(self, name, salary, tool):
        super().__init__(name, salary)
        self.tool = tool

    def design(self):
        print(f"{self.name} is designing using {self.tool}.")


print("--- 10. Complete Real-World Example ---")
dev = Developer("Mrunmay", 120000, "Python")
des = Designer("Nisha", 95000, "Figma")

dev.show_details()
dev.give_raise(10000)
dev.code()
print()

des.show_details()
des.design()
print()

Developer.company_info()
Employee.work_hours()
print()


# =============================================================================
# QUICK REFERENCE SUMMARY
# =============================================================================
# Extra note:
# OOP is especially helpful when the program has many related entities,
# such as users, orders, payments, employees, products, cars, or bank accounts.
#
# For very small scripts, OOP may not always be necessary.
# But for medium and large programs, OOP makes the code easier to grow,
# maintain, test, and understand.

"""
Concept          | Meaning                              | Key Syntax
-----------------|--------------------------------------|------------------------------
Class            | Blueprint for objects                | class MyClass:
Object/Instance  | Real thing created from class        | obj = MyClass()
__init__()       | Constructor, runs on object creation | def __init__(self, ...):
self             | Refers to current object             | self.attribute = value
Instance Var     | Data unique to each object           | self.name = name
Class Variable   | Shared across all objects            | class_var = value
Instance Method  | Uses object data                     | def method(self):
Class Method     | Uses class data                      | @classmethod def m(cls):
Static Method    | Independent utility                  | @staticmethod def m():
Encapsulation    | Hiding data using __variable         | self.__balance = 0
Inheritance      | Child reuses parent features         | class Child(Parent):
Polymorphism     | Same method, different behavior      | def sound(self): ...
Abstraction      | Hide complexity via abstract class   | from abc import ABC
"""
