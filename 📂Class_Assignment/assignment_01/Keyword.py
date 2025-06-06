# Keywords            :: 	 Example
# Control Flow               if, elif, else, for, while, break
# Exception Handling         try, except, finally
# Function & Class         	 def, return
# Variable & Scope	         global, nonlocal
# Import & Modules	         import, from, as
# Object-Oriented (OOP)	     class, object

#Control Flow
# if, elif, else, for, while, break, continue, pass
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
    print(f"Iteration {i}")

    # While loop example
count = 0
while count < 5:
    print(f"Count is {count}")
    count += 1
        # Break example
    for i in range(10):
        if i == 5:
            break
    print(f"Break example iteration {i}")

#Exception Handling
# try, except, finally

    try:
        file = open("non_existent_file.txt", "r")
    except FileNotFoundError:
        print("File not found")
    finally:
        print("Finished trying to open the file")
#Function 
# def, return
def add(a, b):
    return a + b

print(add(5, 10))

#Class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age
    
p = Person("Areeba", 25)
print(p.get_name())
print(p.get_age())      

#Variable & Scope
# global, nonlocal
def my_func():
    global x
    x = 10
    print(x)

my_func()
print(x , '1')

def outer():
    x = 10
    def inner():
        nonlocal x
        x = 20
        print(x)
    inner()
    print(x)

outer()

#Logical & Boolean  
# True, False, None, and, or, not, is, in
print(True and False)
print(True or False)
print(not True)
print(5 in [1, 2, 3, 4, 5])

#Import & Modules
# import, from, as  
import math
print(math.sqrt(25))

