# Python Basics Assignment 03

A collection of Python examples covering control flow, loops, and data structures.

## Table of Contents
- [Control Flow & Loops](#control-flow--loops)
- [Lists, Tuples & Dictionaries](#lists-tuples--dictionaries)
- [Sets & Frozensets](#sets--frozensets)
- [Interactive Playground](#interactive-playground)

---

## Control Flow & Loops

**Key Concepts:**  
- `if-else` statements, `for` loops, and conditional logic.

<details>
  <summary><strong>Click to expand examples</strong></summary>

  **Examples:**  
  1. **Voting Eligibility Check**: Uses `if-else` to determine voting eligibility based on age.
  2. **Grade Assignment**: Uses `if-elif-else` inside a loop to assign grades to scores.
  3. **Simple Loop**: Iterates 5 times with `range()`.

  ```python
  # Voting Eligibility Check Example
  age = int(input("Enter your age: "))
  if age >= 18:
      print("You are eligible to vote.")
  else:
      print("You are not eligible to vote.")
  
  # Grade Assignment Example
  scores = [88, 76, 92, 67, 85]
  for score in scores:
      if score >= 90:
          grade = 'A'
      elif score >= 80:
          grade = 'B'
      elif score >= 70:
          grade = 'C'
      else:
          grade = 'D'
      print(f"Score: {score}, Grade: {grade}")
  
  # Simple Loop Example
  for i in range(5):
      print(f"Iteration {i+1}")
