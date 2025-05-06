# Python Object-Oriented Programming Fundamentals

A repository demonstrating core OOP concepts in Python with practical examples.

## Key Concepts

### 🧩 Class & Objects
- **Class**: Blueprint for creating objects (`class Dog:`)
- **Instance**: Specific object created from a class (`my_dog = Dog()`)
- **Constructor**: `__init__` method (initializer)
- **Destructor**: `__del__` method (rarely used explicitly)

### 🎛️ Dunder (Magic) Methods
Double-underscore methods for operator overloading:
- `__init__`: Object initialization
- `__str__`: String representation
- `__repr__`: Official string representation
- `__del__`: Destructor (automatic garbage collection)

### 🔧 Attributes
- **Instance Attributes**: Unique to each object (`self.name`)
- **Class Attributes**: Shared across all instances (`species = "Canine"`)

## Code Example
```python
class Animal:
    # Class attribute
    kingdom = "Animalia"

    # Constructor
    def __init__(self, name):
        # Instance attribute
        self.name = name

    # Dunder method
    def __str__(self):
        return f"{self.name} ({self.kingdom})"

    # Destructor
    def __del__(self):
        print(f"{self.name} object destroyed")

# Instance creation
lion = Animal("Simba")
print(lion)  # Uses __str__