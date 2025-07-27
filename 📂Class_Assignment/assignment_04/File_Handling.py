# File handling in Python
# Open a file
# Read a file (r)
# Write a file (w)
# Append a file (a)

# Define constant for filename to avoid duplication
FILENAME = 'demo.txt'

# Example with raw open/close (writing to file.txt)
file = open("file.txt", "w")
file.write("Hello World")
file.close()

# Example with appending to new_file.txt
lines = ["Areeba\n", "Irfan\n", "Python\n"]
file = open("new_file.txt", "a")
file.writelines(lines)
file.close()

# Example with context manager (with statement)
with open(FILENAME, 'w') as file:
    file.write('Python File Handling\n')
    file.write('Line 2\n')

with open(FILENAME, 'r') as file:
    print('Content:')
    print(file.read())

with open(FILENAME, 'a') as file:
    file.write('Appended Line\n')

with open(FILENAME, 'r') as file:
    file.seek(0)
    print('First line:', file.readline())
