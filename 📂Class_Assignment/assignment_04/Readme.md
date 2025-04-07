# 🌟 CLASS-04-ASSIGNMENT 🌟

Welcome to **Class 04 Assignment**! This project covers essential Python concepts, including **Control Module Functions, Exception Handling, File Handling, and Math/Date-Time Operations**.  

---

## 📚 **TOPICS COVERED**  

### 🎛️ **Control Module Function**  
- **Modules in Python** (functions, classes, variables)  
- **Types of Python Modules**  
- **Functions in Python**  
- **Scope of Variables**  

### ⚠️ **Exception Handling**  
- `try` Block  
- `except` Block  
- `else` Block  
- `finally` Block  

### 📂 **File Handling**  
- Opening a File (`open()`)  
- Reading (`'r'` mode)  
- Writing (`'w'` mode)  
- Appending (`'a'` mode)  

### 📅 **Math & Date-Time**  
- `time` module  
- `datetime` module  
- `calendar` module  

---

## 🚀 **USAGE**  

### **Control Module Function**  
```python
import math  # Example module
def greet():
    print("Hello from a function!")

greet()
```

### **Exception Handling**
```
try:
    x = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
finally:
    print("Execution complete.")
```
### **File Handling**
# Writing to a file
```
with open("example.txt", "w") as file:
    file.write("Hello, World!")
```
# Reading from a file
```
with open("example.txt", "r") as file:
    print(file.read())

```
### **Math & Date-Time**
```
import datetime
now = datetime.datetime.now()
print("Current date and time:", now)
```
### **🌈 FEATURES**

✔ Modular Code Structure
✔ Error Handling Best Practices
✔ Efficient File Operations
✔ Date & Time Manipulation

### **📜 LICENSE**
This project is open-source under the MIT License.

## **✨ CONTRIBUTE**
Feel free to fork, open issues, or submit PRs!

Happy Coding! 