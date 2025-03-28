# Ask the user for two numbers, one at a time, and then print the result of dividing the first number by the second and also the remainder of the division.

# Here's a sample run of the program (user input is in bold italics):

# Please enter an integer to be divided: 5

# Please enter an integer to divide by: 3

# The result of this division is 1 with a remainder of 2

def main():
    divided : float = float(input("Ente an integer to be divided: "))
    divider: float = float(input("Enter an integer to divide by : "))
    result: float = divided // divider
    remainder: float = divided % divider
    print(f"The result of this division is {result} with a remainder of {remainder}")

# This provided line is required at the end of
# Python file to call the main() function.
if __name__ == '__main__':
    main()