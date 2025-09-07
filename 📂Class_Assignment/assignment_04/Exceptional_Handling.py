# Exception Handling (with try, except, else, and finally)

DIVIDE_BY_ZERO_MSG = "Cannot divide by zero"  # ✅ Defined constant

# Try Block
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f'An error occurred: {DIVIDE_BY_ZERO_MSG}')
    # raise  # Uncomment to re-raise the exception if needed

# Except Block
try:
    result = 10 / 0
except ZeroDivisionError:
    print(DIVIDE_BY_ZERO_MSG)
except Exception as e:
    print(f'An unexpected error occurred: {e}')

# Else Block
try:
    result = 10 / 5
except ZeroDivisionError:
    print(DIVIDE_BY_ZERO_MSG)
else:
    print(f'Division successful: {result}')

# Finally Block
try:
    result = 10 / 0
except ZeroDivisionError:
    print(DIVIDE_BY_ZERO_MSG)
finally:
    print('This will always execute')
