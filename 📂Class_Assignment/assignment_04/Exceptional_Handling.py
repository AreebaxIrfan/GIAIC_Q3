#Exceptional Handling (with try, except, else, and finally)
#Try Block

try:
    result = 10 / 0
except:
    print('an error occurred')

#Except Block
try:
    result = 10 / 0
except ZeroDivisionError:
    print('Cannot divide by zero')
except Exception as e:
    print(f'An un expected error occured :{e}')

#Else Block


try:
    result = 10 / 5
except ZeroDivisionError:
    print('Cannot divide by zero')
else:
    print(f'Division successful:{result}')

#Finally Block
try:
    result = 10 / 0
except ZeroDivisionError:
    print('Cannot divide by zero')
finally:
    print('This will always excute')

