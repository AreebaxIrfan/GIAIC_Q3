def add_greeting(cls):
    def greet(self):
        return "Hello from Decorator!"
    cls.greet = greet  # Add greet method to class
    return cls

@add_greeting
class Person:
    def __init__(self, name):
        self.name = name

# Example usage
person = Person("Areeba Irfan")
print(person.greet())