# class-04
## Control Flow & Data Types

# Comparison Operators: ==, !=, >, >=, <=

x: int = 10
y: int = 20

print("x == y =", x == y)
print("x != y =", x != y)
print("x > y =", x > y)
print("x >= y =", x >= y)
print("x < y =", x < y)

# Logical Operators (Demonstrated in if conditions below)

# if Statement
name = "Areeba"
if name == "Areeba":
    print("Hello")

# else Statement
a = 10
if a == 10:
    print("hello")
else:
    print("world")

# elif Statement
age = 18
if age > 18:
    print("You are eligible for the student discount")
elif age < 18:
    print("Try next time")
else:
    print("Oops! Something went wrong")

# Nested if Statement
num: int = 10
if num > 0:
    if num % 2 == 0:
        print("The number is positive and even")
    else:
        print("The number is positive and odd")
else:
    print("The number is negative")

# -------------------------
# Lists, Tuples, Dictionary
# -------------------------

# Lists
fruits: list = ["apple", "banana", "cherry"]
numbers: list = [10, 20, 30, 40]
mixed: list = ["hello", 42, 3.24, True]

print("fruits =", fruits)
print("numbers =", numbers)
print("mixed =", mixed)

# Modify element in list
fruits[-3] = "watermelon"
print("Modified fruits list =", fruits)

# Tuples
tuple_1: tuple = tuple(["apple", "banana", "cherry"])
tuple_2: tuple = (10, 20, 30)
mixed_tuple: tuple = ("hello", 42, 3.14, True)

print("tuple_1 =", tuple_1)
print("tuple_2 =", tuple_2)

# Memory check for tuples
tuple1: tuple = (10, 20, 30)
tuple2: tuple = (10, 20, 30)

print("id(tuple1):", id(tuple1))
print("id(tuple2):", id(tuple2))

# Dictionary
thedict: dict = {
    "name": "Areeba Irfan",
    "age": 18,
    "country": "Pakistan"
}

print("Country:", thedict["country"])
print("Name:", thedict["name"])

# -----------------
# Set Data Types
# -----------------

my_set: set = {123, 454, 5, 6}

# Correct set creation: must not use list inside curly braces
my_set2: set = set([123, 452, 5, 6])

# Empty set
unknown: dict = {}         # This creates an empty dictionary, not a set
empty_set: set = set()     # This is how to create an empty set

print("my_set =", my_set)
print("my_set2 =", my_set2)
print("type of my_set2 =", type(my_set2))

# Sets are unordered and unindexable
my_Set: set = {1, 2, 3, 4, 5}
try:
    my_Set[0] = 10
except TypeError as e:
    print("Error:", e)
