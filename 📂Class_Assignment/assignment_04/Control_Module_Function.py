##Module in Python (function, classes, variables)
#Types of Python Modules
#1. Built-in Modules
import math
print(math.sqrt(16))
#2. User-defined Modules
def add(a, b):
    return a + b
#3. Third-party Modules
import requests
response = requests.get("https://www.google.com")
print(response.status_code)


#Function in Python

def my_function():
    print("Hello from a function")
my_function()

#Function Argument
def greeting(name):
    "This is a greeting function"
    print("Hello, " + name)
    return
greeting("Areeba Irfan")

#Scope of Varaible

total = 0

def sum (arg1, arg2):
    total = arg1 + arg2
    print("Inside the function local total : ", total)
    return total
sum (10 ,20)
print("Outside the function global total : ", total) 
