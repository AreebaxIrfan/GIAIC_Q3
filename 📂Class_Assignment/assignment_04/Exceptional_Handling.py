# Exception Handling (with try, except, else, and finally)
# Try Block
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print('An error occurred: Cannot divide by zero')
    # raise  # Uncomment to re-raise the exception if needed

# Except Block
try:
    result = 10 / 0
except ZeroDivisionError:
    print('Cannot divide by zero')
except Exception as e:
    print(f'An unexpected error occurred: {e}')

# Else Block
try:
    result = 10 / 5
except ZeroDivisionError:
    print('Cannot divide by zero')
else:
    print(f'Division successful: {result}')

# Finally Block
try:
    result = 10 / 0
except ZeroDivisionError:
    print('Cannot divide by zero')
finally:
    print('This will always execute')
