# ------------------- Control Flow -------------------
x = 10
y = 20

if x > y:
    print("x is greater than y")
elif x < y:
    print("x is less than y")
else:
    print("x is equal to y")

# For loop example
for i in range(5):
    print(f"For loop iteration {i}")

# While loop example
count = 0
while count < 5:
    print(f"While loop count is {count}")
    count += 1

# Break example
for i in range(10):
    if i == 5:   # break when i reaches 5
        print("Breaking the loop at i = 5")
        break
    print(f"Break example iteration {i}")

# ------------------- Exception Handling -------------------
try:
    file = open("non_existent_file.txt", "r")
except FileNotFoundError:
    print("File not found")
finally:
    print("Finished trying to open the file")

# ------------------- Function -------------------
def add(a, b):
    return a + b

print("Add function result:", add(5, 10))

# ------------------- Class -------------------
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

p = Person("Areeba", 25)
print("Person name:", p.get_name())
print("Person age:", p.get_age())

# ------------------- Variable & Scope -------------------
x = 10   # global variable

def my_func():
    global x
    x = 50   # change global x so it's not constant
    print("Inside my_func, x =", x)

my_func()
print("Outside my_func, global x =", x)

def outer():
    x = 10
    def inner():
        nonlocal x
        x = 20   # modifies the outer function's variable
        print("Inside inner, x =", x)
    inner()
    print("Inside outer after inner call, x =", x)

outer()

# ------------------- Logical & Boolean -------------------
print("Logical and:", True and False)
print("Logical or:", True or False)
print("Logical not:", not True)
print("Membership test (5 in list):", 5 in [1, 2, 3, 4, 5])

# ------------------- Import & Modules -------------------
import math
print("Square root of 25:", math.sqrt(25))
