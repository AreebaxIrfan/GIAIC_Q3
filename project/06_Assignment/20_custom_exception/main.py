class InvalidAgeError(Exception):
    """Custom exception for invalid age input."""
    pass

class Person:
    def __init__(self, name, age):
        self.name = name
        self._age = None
        self.set_age(age)
        
    def set_age(self, age):
        """"Validate and set the age , raising InvalidAgeError if age < 18 ."""
        if age < 18 :
            raise InvalidAgeError(f"Invalid age {age}. Age must be 18 or older.")
        self._age = age
        
    def get_age(self):
        """Return the age."""
        return self._age
try:
    person1 = Person("Areeba Irfan", 17)
    print(f"Name: {person1.name}, Age: {person1.get_age()}")
    person2 = Person("John Doe", 10)
except InvalidAgeError as e:
    print(f'Error: {e}')
    
