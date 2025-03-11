#Logical Operations
#Logical operators are used to combine conditional statements.

# and , or , not
# and : Returns True if both statements are true
# or : Returns True if one of the statements is true
# not : Reverse the result, returns False if the result is true
# Example
# Test if a is greater than b, AND if c is greater than a:
a = 200
b = 33
c = 500
if a > b and c > a:
   print("Both conditions are True")
# Example
# Test if a is greater than b, OR if a is greater than c:
a = 200
b = 33
c = 500
if a > b or a > c:
   print("At least one of the conditions is True")
# Example
# Reverse the result:
a = 200
b = 33
if not a > b:
   print("a is not greater than b")