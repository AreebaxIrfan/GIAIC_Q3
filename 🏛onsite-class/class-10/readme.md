# Python Object-Oriented Programming Concepts

This repository provides explanations and examples of key object-oriented programming (OOP) concepts in Python, including **class vs. instance variables**, **composition vs. aggregation**, and **method resolution order (MRO)**. These concepts are essential for effective OOP design and understanding Python's inheritance mechanisms.

## Table of Contents
- [Class vs. Instance Variables](#class-vs-instance-variables)
- [Composition vs. Aggregation](#composition-vs-aggregation)
- [Method Resolution Order (MRO)](#method-resolution-order-mro)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Class vs. Instance Variables
- **Class Variables**: Shared across all instances of a class. Used to store data or behavior common to all objects of the class.
- **Instance Variables**: Unique to each object. Allow individual objects to maintain their own state.
- **Key Insight**: Understanding the distinction ensures proper data management in OOP.

## Composition vs. Aggregation
- **Composition** (Strong "part of" relationship):
  - One class owns another, e.g., a `Car` owns an `Engine`.
  - If the parent object (e.g., `Car`) is destroyed, the owned object (e.g., `Engine`) is also destroyed.
  - Example: The `Engine` cannot exist independently of the `Car`.
- **Aggregation** (Weak "connected to" relationship):
  - One class is linked to another, e.g., a `School` has `Students`.
  - The linked objects (e.g., `Students`) can exist independently of the parent (e.g., `School`).
  - Example: If the `School` is deleted, `Students` still exist.

## Method Resolution Order (MRO)
- **MRO** defines the order in which Python searches for methods and attributes in a class hierarchy, especially in **multiple inheritance**.
- Used to resolve conflicts when multiple parent classes define the same method or attribute.
- Python uses the **C3 linearization algorithm** to compute MRO.
- Example: In a diamond inheritance scenario, MRO ensures the correct method is called based on the inheritance order.
- Access MRO via `ClassName.mro()` or `__mro__`.

## Examples
The repository includes Python code examples demonstrating:
1. **Composition**: A `Car` class owning an `Engine` object.
2. **Aggregation**: A `School` class linked to `Student` objects.
3. **MRO**: A diamond inheritance structure with classes `A`, `B`, `C`, and `D`, showing how Python resolves method calls.
